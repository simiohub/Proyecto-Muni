from django.shortcuts import render

from .models import Servicio


def cargar_servicios():
    return Servicio.objects.all().order_by('id')


def clasificar_plazo(dias):
    if dias <= 3:
        return 'corto'
    elif dias <= 7:
        return 'medio'
    else:
        return 'largo'


def inicio(request):
    servicios = cargar_servicios()

    gratuitos = servicios.filter(gratuito=True).count()
    pagados = servicios.filter(gratuito=False).count()

    data = {
        'titulo': 'Servicios a la Comunidad',
        'total': servicios.count(),
        'gratuitos': gratuitos,
        'pagados': pagados,
    }
    return render(request, 'servicios/inicio.html', data)


def listado(request):
    servicios = cargar_servicios()

    categoria = request.GET.get('categoria', '')
    filtrados = servicios.filter(categoria=categoria) if categoria else servicios

    categorias = list(Servicio.objects.values_list('categoria', flat=True).distinct())
    categorias = sorted(categorias)

    for servicio in filtrados:
        servicio.clasificacion = clasificar_plazo(servicio.plazo_dias)

    data = {
        'titulo': 'Listado de Servicios',
        'servicios': filtrados,
        'categoria': categoria,
        'categorias': categorias,
        'conteo': filtrados.count(),
    }
    return render(request, 'servicios/listado.html', data)