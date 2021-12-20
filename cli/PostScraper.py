import asyncio
import aiohttp

from lposts.models import Post

class PostScraper:
    def __init__(self):
        pass

    async def _scrapeTechCrunch(self):
        pass

    async def _scrapeMedium(self):
        pass

    async def run(self):
        cos = (
            self._scrapeTechCrunch(),
            self._scrapeMedium(),
        )
        await asyncio.gather(*cos)
