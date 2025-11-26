import os
import sys
from pathlib import Path

# Ensure project root is on sys.path so Django settings package is importable
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE','bookStore.settings')
import django
django.setup()
from django.test import Client

c = Client()
paths = ['/', '/books/', '/books/1/', '/authors/1/']
for p in paths:
    r = c.get(p)
    print(p, r.status_code)
