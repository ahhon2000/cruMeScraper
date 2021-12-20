import asyncio
import aiohttp
from pathlib import Path
from bs4 import BeautifulSoup
from more_itertools import islice_extended

import dateutil.parser
import datetime
import pytz

from lposts.models import Post
from cruMeScraper.settings import LPOSTS

class PostScraper:
    def __init__(self):
        pass

    async def _scrapeTechCrunch(self):
        f = Path(__file__).resolve().parent / 'latest_techCrunch.html'
        cnt = f.read_text()
        soup = BeautifulSoup(markup=cnt, features='lxml')

        nScraped = 0
        for p in soup.select('.post-block__header'):
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

            # TODO rm this print
            print(f"""
{title}
    date: {date}
    author: {author}
"""[1:-1])
            nScraped += 1

    async def _scrapeMedium(self):
        pass

    async def run(self):
        cos = (
            self._scrapeTechCrunch(),
            self._scrapeMedium(),
        )
        await asyncio.gather(*cos)
