# cruMeScraper
A web app that shows the latest TechCrunch and Medium blog posts

DESIGN
------

The app consists of two components:
  * A command-line tool that scrapes the latest posts from TechCrunch and Medium.
  * A Django website for displaying the posts.

Scraped data is stored in an SQLite database.


INSTALLATION
------------

The following instructions are for running the app in DEBUG mode on localhost.

1. After cloning the Git repository, create and activate a virtual environment:

  $ cd cruMeScraper/
  $ python3 -m venv venv
  $ . venv/bin/activate

2. Install the dependencies:

  $ pip3 install -r requirements.txt
  
3. Make the initial Django migration:

  $ python3 manage.py migrate


USAGE
-----

Do the following in the virtual environment:

1. Scrape the latest posts by using the script scrapeLatest.py:

  $ python3 cli/scrapeLatest.py
  
2. Start the Django server:

  $ python3 manage.py runserver

3. Go to http://127.0.0.1:8000 in your browser. This page shows the latests posts in 3 subsections:

  * TechCrunch & Medium posts, interleaved.
  * TechCrunch posts.
  * Medium posts.
