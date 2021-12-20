#!/usr/bin/python3

import os, sys
from pathlib import Path
import asyncio

scrPath = Path(__file__).resolve()
scrDir = scrPath.parent
projDir = scrDir.parent

for p in (scrDir, projDir):
    sys.path.append(str(p))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cruMeScraper.settings")

import django
django.setup()

from PostScraper import PostScraper

async def main():
    ps = PostScraper()
    await ps.run()

asyncio.run(main())
