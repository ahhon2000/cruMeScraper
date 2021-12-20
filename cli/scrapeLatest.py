#!/usr/bin/python3

import os, sys
from pathlib import Path

scrPath = Path(__file__).resolve()
scrDir = scrPath.parent
projDir = scrDir.parent

for p in (scrDir, projDir):
    sys.path.append(str(p))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cruMeScraper.settings")

import django
django.setup()

from PostScraper import PostScraper

ps = PostScraper()
ps.run()
