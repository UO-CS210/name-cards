"""Scrapes saved Duckweb html page of student pictures
to produce CSV file of (name, path) pairs where name is
student name and path takes us to JPEG image from the saved
web content, renamed and refiled to make it easier to use in
PDFLaTeX. 

Usage: python3 scrape.py "Class Photos.html" pictures.csv img

  to create a directory "img" with renamed copies of the photos,
  and produce a CSV file that looks like

Name,Picture
"Acheson, Lucy R",img/photo1.jpg
"Adams, Makena M",img/photo2.jpg
"""

import argparse
import io
from dataclasses import dataclass
import csv
import sys
import shutil
import os
import logging

from bs4 import BeautifulSoup

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

@dataclass
class IOSpecs():
    working_dir: str
    html: io.FileIO
    csv: io.FileIO


def cli() -> IOSpecs:
    parser = argparse.ArgumentParser("scrape",
                                     description="Scrape pictures from DuckWeb student pictures")
    parser.add_argument("dir",
                        help="Working directory --- dumped html, photos subdirectory, and output CSV go here",
                        nargs="?", default="data")
    parser.add_argument("html",
                        help="Path to HTML of student pictures, relative to data directory",
                        type=str,
                        nargs="?", default="Class Photos.html")
    parser.add_argument("csv",
                        help="Where to write CSV, relative to data directory",
                        type=str,
                        nargs="?", default="photos.csv")

    args = parser.parse_args()
    try:
        os.makedirs(args.dir, exist_ok=True)
    except Exception:
        print(f"Could not access or create directory {args.dir}", file=sys.stderr)
        sys.exit(1)
    try:
        html_path = os.path.join(args.dir, args.html)
        html_file = open(html_path, "r")
    except Exception:
        print(f"Could not read {args.html} for reading in directory {args.dir}", file=sys.stderr)
        sys.exit(1)
    try:
        csv_path = os.path.join(args.dir, args.csv)
        csv_file = open(csv_path, "w")
    except:
        print(f"Could not open {args.csv} for writing in directory {args.dir}", file=sys.stderr)
        sys.exit(1)

    return IOSpecs(args.dir, html_file, csv_file)


def scrape(soup: BeautifulSoup) -> list[tuple[str, str]]:
    """Extract photos and names from Duckweb "student pictures" page.
    Returns list of (student name, student photo) pairs.
    """
    mugs: list[str, str] = []
    student_photos = soup.findAll('img')
    for img in student_photos:
        # Expecting something like this, table.tbody.tr.td.img
        #   <table class="plaintable">
        #   <tbody><tr>
        #   <td class="pldefault"><img src="./Class Photos_files/hwskclst(10).p_DispImage" height="200" border="0"></td>
        # BUT other images (tabs, logos, etc) are packaged almost the same.
        # Maybe DispImage will tell them apart
        #
        if "DispImage" not in img['src']:
            log.debug(f"Image but not a student photo: {img['src']}")
            continue
        link = img['src']
        log.debug(f"Student photo: {link}")


        # Now I've got what seems to be a student photo,
        # I want to find the student name that goes with it.
        # Expecting this structure:
        # <tbody>
        # <tr><td class="pldefault"><img src="./Class Photos_files/hwskclst.p_DispImage" height="200" border="0"></td></tr>
        # <tr><td class="pldefault">    Acheson, Lucy R </td> </tr>
        # <tr> <td nowrap="nowrap" class="pldefault">951948056</td></tr>
        # </tbody>
        row = img.parent.parent
        if row.name != "tr":
            log.warning(f"Oops, not a student photo: {row.name}..{img['src']}")
            continue
        next_row = row.next_sibling.next_sibling  #Skipping a newline between rows
        log.debug(next_row)
        student_name = next_row.find("td").string.strip()
        log.info(f"Student name: {student_name}")
        mugs.append((student_name, link))
    return mugs

def refile(table: list[tuple[str, str]], dir: str) -> list[tuple[str, str]]:
    """Copies HTML linked files into directory 'dir' with LaTeX-compatible names,
    which replace old names in the input table.
    Effect:  Files copied into dir, which will be created if not present
    Result:  Table with file names replaced by copied file names
    """
    if not(os.path.isdir(dir)):
        os.makedirs(dir)
        # Crash if directory can't be created, e.g., if it is a normal file

    serial = 0
    result: list[tuple[str, str]] = []
    for name, link in table:
        serial += 1
        new_filename = f"{dir}/photo{serial}.jpg"
        shutil.copy(os.path.join(dir, link), new_filename)
        result.append((name, new_filename))
    return result

def dump_csv(table: list[tuple[str, str]], file):
    """Dump the table as a CSV file"""
    writer = csv.writer(file)
    writer.writerow(["Name", "Picture"])
    for row in table:
        writer.writerow(row)


def main():
    where = cli()
    with where.html as raw:
        soup = BeautifulSoup(raw)
    mugs = scrape(soup)
    refiled = refile(mugs, where.working_dir)
    dump_csv(refiled, where.csv)
    where.csv.close()

if __name__ == "__main__":
    main()