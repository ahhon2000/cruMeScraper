#!/usr/bin/python3

import os, sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cruMeScraper.settings")

import django
django.setup()

import lposts.models
