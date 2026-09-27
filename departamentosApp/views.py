from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Departamento


def cargar_departamentos():
    return Departamento.objects.all().order_by('id')


def inicio(request):
    departamentos = cargar_departamentos()
    total = departamentos.count()
    altas = departamentos.filter(prioridad='alta').count()
    proporcional = (altas / total) * 100 if total > 0 else 0

    data = {
        'titulo': 'Departamentos Municipales',
        'total': total,
        'cantidad_altas': altas,
        'porcentaje_prioritarios': round(proporcional, 1),
    }
    return render(request, 'departamentos/inicio.html', data)


def listado(request):
    departamentos = cargar_departamentos()

    prioridad = request.GET.get('prioridad', '')
    filtrados = departamentos.filter(prioridad=prioridad) if prioridad else departamentos

    por_prioridad = {
        'alta': Departamento.objects.filter(prioridad='alta').count(),
        'media': Departamento.objects.filter(prioridad='media').count(),
        'baja': Departamento.objects.filter(prioridad='baja').count(),
    }

    data = {
        'titulo': 'Listado de Departamentos',
        'departamentos': filtrados,
        'prioridad': prioridad,
        'conteo': filtrados.count(),
        'por_prioridad': por_prioridad,
    }
    return render(request, 'departamentos/listado.html', data)


def detalle(request, departamento_id):
    departamento = get_object_or_404(Departamento, id=departamento_id)

    data = {
        'titulo': departamento.nombre,
        'departamento': departamento,
    }
    return render(request, 'departamentos/detalle.html', data)