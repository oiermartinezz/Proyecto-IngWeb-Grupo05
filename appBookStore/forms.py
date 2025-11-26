from django import forms
from django.core.exceptions import ValidationError
import re
from typing import Any, Optional
from .models import Book, Publisher


class BookSearchForm(forms.Form):
    """Formulario de búsqueda y filtrado de libros con validaciones de seguridad."""
    
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
        queryset=Publisher.objects.none(),
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

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # type: ignore permite ignorar el warning de Pylance sobre queryset
        self.fields['publisher'].queryset = Publisher.objects.all()  # type: ignore[attr-defined]
    
    def clean_search(self) -> str:
        """Validar que el search no contiene caracteres maliciosos."""
        search = self.cleaned_data.get('search', '')
        if search:
            # Prevenir inyecciones SQL simples y XSS
            dangerous_chars = ['<', '>', '"', "'", ';', '--']
            if any(char in search for char in dangerous_chars):
                raise ValidationError(
                    "La búsqueda contiene caracteres no permitidos.",
                    code='invalid_chars'
                )
        return search


class NewsletterSubscriptionForm(forms.Form):
    """Formulario de suscripción al newsletter con validaciones robustas."""
    
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
    
    def clean_name(self) -> str:
        """Validar que el nombre no contiene caracteres maliciosos."""
        name = self.cleaned_data.get('name', '')
        if name:
            # Solo permitir letras, espacios y puntos
            pattern = r"^[a-záéíóúñA-ZÁÉÍÓÚÑ\s.'-]+$"
            if not re.match(pattern, name):
                raise ValidationError(
                    "El nombre contiene caracteres no permitidos.",
                    code='invalid_name'
                )
        return name
    
    def clean_email(self) -> str:
        """Validar email con restricciones adicionales."""
        email = self.cleaned_data.get('email', '')
        if email and len(email) > 254:
            raise ValidationError(
                "El email es demasiado largo.",
                code='email_too_long'
            )
        return email


