from pathlib import Path
from bs4 import BeautifulSoup
from more_itertools import islice_extended
from threading import Thread

import dateutil.parser
import datetime
import pytz

from lposts.models import Post
from cruMeScraper.settings import LPOSTS

class PostScraper:
    def __init__(self):
        pass

    def _scrapeTechCrunch(self):
        f = Path(__file__).resolve().parent / 'latest_techCrunch.html'
        cnt = f.read_text()
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
                )
                post.save()

            # TODO rm this print
            print(f"""

{title}
    date: {date}
    author: {author}
    img: {img}
    excerpt: {excerpt}
"""[1:-1])

    def _scrapeMedium(self):
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
