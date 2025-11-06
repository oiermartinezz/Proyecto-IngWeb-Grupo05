from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render
from .models import Publisher, Author, Book

def index(request):
    #la portada con un libro reciente de cada editorial

    publishers = Publisher.objects.all()
    editoriales_con_libro = {}

    for publisher in publishers:
        # Por cada editorial, busca el libro más reciente 
        libro_reciente = publisher.book_set.order_by('-publication_date').first()
        editoriales_con_libro[publisher] = libro_reciente

    context = {'editoriales': editoriales_con_libro}
    return render(request, 'index.html', context)


# Vista para la lista de Libros (books.html)
def book_list(request):
    
    #Muestra el listado de todos los libros.
    
    libros = Book.objects.all().order_by('title')
    context = {'libros': libros}
    return render(request, 'books.html', context)


# Vista para el detalle de un Libro (book.html)
def book_detail(request, book_id):
    
    # los detalles de un libro específico, incluyendo su editorial y autores.
    
    libro = get_object_or_404(Book, pk=book_id)
    autores = libro.authors.all()
    context = {'libro': libro, 'autores': autores}
    return render(request, 'book.html', context)


# Vista para la lista de Editoriales (publishers.html)
def publisher_list(request):
    
   #Muestra el listado de todas las editoriales.
    
    editoriales = Publisher.objects.all().order_by('name')
    context = {'editoriales': editoriales}
    return render(request, 'publishers.html', context)


# Vista para el detalle de una Editorial (publisher.html)
def publisher_detail(request, publisher_id):
    
    #Muestra los detalles de una editorial específica y todos sus libros.
    
    editorial = get_object_or_404(Publisher, pk=publisher_id)
    libros = editorial.book_set.all().order_by('title')
    context = {'editorial': editorial, 'libros': libros}
    return render(request, 'publisher.html', context)


# Vista para la lista de Autores (authors.html)
def author_list(request):
    
    #Muestra el listado de todos los autores.
    
    autores = Author.objects.all().order_by('name')
    context = {'autores': autores}
    return render(request, 'authors.html', context)


# Vista para el detalle de un Autor (author.html)
def author_detail(request, author_id):

    #Muestra los detalles de un autor específico y todos sus libros.
    
    autor = get_object_or_404(Author, pk=author_id)
    libros = autor.book_set.all().order_by('title')
    context = {'autor': autor, 'libros': libros}
    return render(request, 'author.html', context)