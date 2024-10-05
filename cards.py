"""Given a CSV file that looks like this:

Name,Picture
"Acheson, Lucy R",img/photo1.jpg
"Adams, Makena M",img/photo2.jpg

Produces a LaTeX file that, when processed with pdflatex,
will create flash cards for learning student names.

Designed to be compatible with scrape.py, which creates CSV file and directory
of pictures from a dumped DuckWeb class pictures page.
"""

import csv
import io
import sys
import argparse
from io import IOBase

## LaTeX template

PROLOG = r"""
\documentclass[frontgrid,letterpaper,12pt]{flacards}
\usepackage{graphicx}
\pagesetup{2}{4}

% \renewcommand{\cardtextstylef}{}
\renewcommand{\cardtextstyleb}{\huge}
\renewcommand{\frfoot}{}
\renewcommand{\brfoot}{CS 211}

\begin{document}
"""

CODA = r"""
\end{document}
"""

def card(name: str, img_path: str) -> str:
    LB, RB = "{", "}"
    BS = "\\"
    surname, given = name.split(",")
    return (f"{BS}card{LB}{BS}includegraphics[height=.20{BS}textheight]"
            +f"{LB}{img_path}{RB}{RB}"
            +f"{LB}{given}{BS}{BS}{surname}{RB}")

def write_cards(table: list[tuple[str, str]], latex_file: IOBase):
    """Writes (pdf)LaTeX flashcards source file from table

    Note that the links from LaTeX file will be correct or not depending on
    the current working directory from which LaTeX is invoked.  Using defaults
    (everything in "data" directory), LaTeX should be invoked from directory in which
    the scripts live, one level up from the data directory.
    """
    print(PROLOG, file=latex_file)
    for name, picture in table:
        print(card(name, picture), file=latex_file)
    print(CODA, file=latex_file)




def read_cards_csv(csv_file) -> list[tuple[str, str]]:
    """Read the CSV file (as produced by scrape.py) into
    a table in which each row is a (name, image path) pair.
    """
    reader = csv.DictReader(csv_file)
    table = []
    for row in reader:
        table.append((row['Name'], row['Picture']))
    return table


def cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser("scrape",
                                     description="Scrape pictures from DuckWeb student pictures")
    parser.add_argument("csv",
                        help="Path to csv linking names to (default stdin)",
                        type=argparse.FileType("r"),
                        nargs="?", default="data/photos.csv")
    parser.add_argument("latex",
                        help="Where to write LaTeX file (if not stdout)",
                        type=argparse.FileType("w"),
                        nargs="?", default="data/cards.tex")
    args = parser.parse_args()
    return args

def main():
    args = cli()
    table = read_cards_csv(args.csv)
    write_cards(table, args.latex)

if __name__ == "__main__":
    main()
