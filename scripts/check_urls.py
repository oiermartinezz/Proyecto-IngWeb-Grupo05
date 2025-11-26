import urllib.request

urls = [
    'http://127.0.0.1:8000/',
    'http://127.0.0.1:8000/books/',
    'http://127.0.0.1:8000/books/1/',
    'http://127.0.0.1:8000/authors/1/',
]

for u in urls:
    try:
        r = urllib.request.urlopen(u, timeout=5)
        print(f"{u} -> {r.getcode()}")
    except Exception as e:
        print(f"{u} -> ERROR: {e}")
