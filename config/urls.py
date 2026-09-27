from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


def index(request):
    data = {
        'titulo': 'Portal Municipal',
        'subtitulo': 'Información organizada de departamentos y servicios municipales',
    }
    return render(request, 'index.html', data)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('departamentos/', include('departamentosApp.urls')),
    path('servicios/', include('serviciosApp.urls')),
]