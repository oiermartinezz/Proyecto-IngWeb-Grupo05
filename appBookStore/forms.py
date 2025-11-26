from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Book

class BookSearchForm(forms.Form):
    """Formulario de búsqueda y filtrado de libros"""
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por título o ISBN...',
            'aria-label': 'Búsqueda de libros'
        })
    )
    publisher = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label='Todas las editoriales',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    min_stock = forms.IntegerField(
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Stock mínimo',
            'aria-label': 'Stock mínimo'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Publisher
        self.fields['publisher'].queryset = Publisher.objects.all()
    
    def clean_search(self):
        """Validar que el search no contiene caracteres maliciosos"""
        search = self.cleaned_data.get('search')
        if search:
            # Prevenir inyecciones SQL simples y XSS
            if any(char in search for char in ['<', '>', '"', "'", ';', '--']):
                raise ValidationError("La búsqueda contiene caracteres no permitidos.")
        return search


class NewsletterSubscriptionForm(forms.Form):
    """Formulario de suscripción al newsletter"""
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@email.com',
            'aria-label': 'Correo electrónico'
        })
    )
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre',
            'aria-label': 'Nombre'
        })
    )
    subscribe_to_news = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Deseo recibir novedades sobre libros'
    )
    
    def clean_name(self):
        """Validar que el nombre no contiene caracteres maliciosos"""
        name = self.cleaned_data.get('name')
        if name:
            # Solo permitir letras, espacios y puntos
            if not re.match(r"^[a-záéíóúñA-ZÁÉÍÓÚÑ\s.'-]+$", name):
                raise ValidationError("El nombre contiene caracteres no permitidos.")
        return name
    
    def clean_email(self):
        """Validar email"""
        email = self.cleaned_data.get('email')
        if email:
            # Validación básica adicional
            if len(email) > 254:
                raise ValidationError("El email es demasiado largo.")
        return email

