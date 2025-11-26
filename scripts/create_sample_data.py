import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE','bookStore.settings')
import django
django.setup()

from appBookStore.models import Publisher, Author, Book
from datetime import date

# Create sample publisher
pub, created = Publisher.objects.get_or_create(name='Editorial Prueba', defaults={'description':'Editorial para pruebas'})
# Create sample author
auth, created = Author.objects.get_or_create(name='Autor Prueba', defaults={'biography':'Biografía de prueba'})
# Create sample book
book, created = Book.objects.get_or_create(title='Libro de Prueba', defaults={'publication_date':date(2020,1,1), 'publisher':pub, 'stock':5})
# Ensure author linked
book.authors.add(auth)
book.save()

print('Created/ensured sample data:')
print('Publisher id:', pub.id)
print('Author id:', auth.id)
print('Book id:', book.id)
