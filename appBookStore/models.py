from django.db import models

# Create your models here.

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to='publisher_logos/', null=True, blank=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    
    name = models.CharField(max_length=50)
    biography = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='author_photos/', null=True, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    # Un libro pertenece a una categoría solo
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)

    # Un libro puede tener varios autores
    authors = models.ManyToManyField(Author)

    title = models.CharField(max_length=100)
    publication_date = models.DateField()

    stock = models.IntegerField(default=0)

    isbn = models.CharField(max_length=20, null=True, blank=True)

    summary = models.TextField(null=True, blank=True)

    #foto de portada de los libros
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)

    def __str__(self):
        return self.title
