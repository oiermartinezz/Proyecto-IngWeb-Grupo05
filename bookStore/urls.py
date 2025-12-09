"""
URL configuration for bookStore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from appBookStore import views

#para las imagenes
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path("newsletter/subscribe/", views.newsletter_subscribe, name="newsletter_subscribe"),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('appBookStore.urls')),
)

# Servir media y estáticos FUERA de i18n_patterns para que no tengan prefijo de idioma
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Servir ficheros estáticos en desarrollo
    try:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    except Exception:
        # En caso de que STATICFILES_DIRS no esté configurado como lista accesible
        pass

