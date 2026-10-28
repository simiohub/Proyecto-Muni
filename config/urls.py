from django.urls import path, include
from django.shortcuts import render


def index(request):
    data = {
        'titulo': 'Portal Municipal',
        'subtitulo': 'Información organizada de departamentos y servicios municipales',
    }
    return render(request, 'index.html', data)


urlpatterns = [
    path('', index, name='index'),
    path('cuentas/', include('accountsApp.urls')),
    path('departamentos/', include('departamentosApp.urls')),
    path('servicios/', include('serviciosApp.urls')),
]