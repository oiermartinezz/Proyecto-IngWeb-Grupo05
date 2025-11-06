from django.urls import path
from . import views

urlpatterns = [
    # listado de categorías
    path('', views.index, name='index'),

    # Lista de Libros
    path('books/', views.book_list, name='book-list'),
    
    # Detalle de un Libro
    path('books/<int:book_id>/', views.book_detail, name='book-detail'),

    # Lista de Editoriales
    path('publishers/', views.publisher_list, name='publisher-list'),

    # Detalle de una Editorial
    path('publishers/<int:publisher_id>/', views.publisher_detail, name='publisher-detail'),

    # Lista de Autores
    path('authors/', views.author_list, name='author-list'),

    # Detalle de un Autor
    path('authors/<int:author_id>/', views.author_detail, name='author-detail'),
]
