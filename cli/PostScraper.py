from pathlib import Path
from bs4 import BeautifulSoup
from more_itertools import islice_extended
from threading import Thread

import requests

import dateutil.parser
import dateparser
import datetime
import pytz

import re

from lposts.models import Post
from cruMeScraper.settings import LPOSTS

class PostScraper:
    URL_TC = 'https://techcrunch.com'
    URL_ME = 'https://medium.com/tag/news/latest'

    def __init__(self):
        pass

    def _download(self, url):
        req = requests.get(url)
        code = req.status_code
        if code != 200: raise Exception(f'failed to download the page: {url} (code={code})')

        return req.content

    def _scrapeTechCrunch(self):
        #f = Path(__file__).resolve().parent / 'latest_techCrunch.html'
        #cnt = f.read_text()
        cnt = self._download(self.URL_TC)

        soup = BeautifulSoup(markup=cnt, features='lxml')

        nScraped = 0
        #for p in soup.select('.post-block__header'):
        for p in soup.select('.post-block'):
            if nScraped >= LPOSTS['N_POSTS']: break

            title = (p.select('.post-block__title') or [None])[0]
            if not title: continue
            title = title.text.strip()

            authors = p.select('.river-byline__authors')
            author = authors[0].text.strip() if authors else 'Unknown Author'

            date = (p.select('.river-byline__time') or [None])[0]
            if date:
                date = date.attrs.get('datetime')
                try:
                    date = dateutil.parser.parse(date)
                except dateutil.parser.ParserError:
                    date = None
            if not date:
                date = datetime.datetime.now(tz=pytz.UTC)

            excerpt = (p.select('.post-block__content') or [''])[0]
            if excerpt:
                excerpt = excerpt.text.strip()

            img = (p.select('.post-block__media img') or [''])[0]
            if img:
                img = img.attrs.get('src', '')

            nScraped += 1

            if not Post.objects.filter(title=title, author=author):
                post = Post(
                    title = title, author = author, article_date = date,
                    excerpt = excerpt, img_link = img,
                    source = 'TC',
                )
                post.save()

    def _scrapeMedium(self):
        #f = Path(__file__).resolve().parent / 'latest_medium.html'
        #cnt = f.read_text()
        cnt = self._download(self.URL_ME)
        soup = BeautifulSoup(markup=cnt, features='lxml')

        nScraped = 0
        ps = soup.select('h4')

        for p in ps:
            for i in range(5): p = p.parent

            title = (p.select('h2') or [None])[0]
            if not title: continue
            title = title.text.strip()

            author = (p.select('h4') or ['Unknown Author'])[0]
            author = author.text.strip()
            if re.search(r'^in$', author, flags=re.IGNORECASE): continue

            img = (p.select('img') or [''])[-1]
            if img:
                img = img.attrs.get('src', '')

            excerpt = (p.select('h3') or [''])[0]
            times = None
            date = None
            if excerpt:
                times = excerpt.nextSibling
                excerpt = excerpt.text.strip()

                ago = (times.select('p') or [None])[0]
                if ago:
                    ago = ago.text.strip()
                    date = dateparser.parse(ago + ' UTC')

            if not date:
                date = datetime.datetime.now(tz=pytz.UTC)

            nScraped += 1

            if not Post.objects.filter(title=title, author=author):
                post = Post(
                    title = title, author = author, article_date = date,
                    excerpt = excerpt, img_link = img,
                    source = 'ME',
                )
                post.save()
                pass

    def run(self):
        Post.objects.all().delete()

        ths = []
        for f in (
            self._scrapeTechCrunch,
            self._scrapeMedium,
        ):
            th = Thread(target=f)
            th.start()
            ths.append(th)

        for th in ths:
            th.join()
