import asyncio

class PostScraper:
    def __init__(self):
        pass

    async def _scrapeTechCrunch(self):
        pass

    async def _scrapeMedium(self):
        pass

    def run(self):
        async def main():
            cos = (
                self._scrapeTechCrunch(),
                self._scrapeMedium(),
            )
            await asyncio.gather(*cos)

        asyncio.run(main())
