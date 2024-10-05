# HOWTO generate name flashcards from Duckweb class photos

0.  Install Beautiful Soup, preferably in a virtual environment. 
    ```commandline
    python3 -m venv env
    . env/bin/activate
    pip install bs4
    ```
    Alternatively, `pip install -r requirements.txt`, which will
    install a compatible version of Beautiful Soup 4, but the most
    recent version (`install bs4`) should work fine. 
1.  In Duckweb, choose "Course Administration Center", choose the 
     term, and choose "View Class Photos" for your class. You 
    should get a page of labeled photos for your students.
    _Note:_ This page contains private or confidential information,
    so I will not show an example, and you must use reasonable care in
    maintaining its confidentiality. 
2. In your browser, save this page. (I use Chrome and have tested 
   this procedure only in Chrome.)  
    ![Save page as](img/SavePage.png)
   Choose "Webpage, Complete" and save in the "data" directory. 
3. Use `scrape.py` to extract a CSV file, like this: 
   ```commandline
   python3 scrape.py
   ```
   Although it is possible to save the HTML page somewhere else and 
   give explicit path names to `scrape.py` and `cards.py`, it is 
   much easier to use the defaults:  The HTML is saved as 
   `data/Class Photos.html` and the accompanying files are saved
    as `data/Class Photos_files`.  That's where `scrape.py` looks by
    default, and by default it saves its output also in `data`.  
   This will include a bunch of JPEG files with names that are easy 
   for LaTeX to digest. 
4. Use `cards.py` to produce `photos.tex` from the `photos.csv` file 
     created by
    `scrape.py`.  Again, you _can_ specify different paths for input 
   and output files, but you probably don't want to. 
5. Run LaTeX on the `data/cards.tex`. Do _not_ cd into the data 
   directory before you run LaTeX, and don't drag the `cards.tex` 
   file icon onto your TeX application, unless you want to take 
   other measures to adjust file locations or names so that the 
   references in `cards.tex` can find the photos.  These 
   references look like 
   ```latex
   \card{\includegraphics[height=.20\textheight]{data/photo3.jpg}}{Given\\Surname}
   ```
   so you should be running LaTeX from the directory _above_ the 
   `data` directory, which is usually the directory where
   `scrape.py` and `cards.py` live.  This directory is where
   `cards.pdf` will be created. 
6. Print `cards.pdf` two-sided, landscape mode, on letter paper. 
   Have fun cutting out the individual cards. 