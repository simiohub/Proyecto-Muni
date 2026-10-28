from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q

from .forms import DepartamentoForm
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


@permission_required('departamentosApp.view_departamento', raise_exception=True)
def gestion_lista(request):
    query = request.GET.get('q', '').strip()
    departamentos = Departamento.objects.all()
    if query:
        departamentos = departamentos.filter(
            Q(nombre__icontains=query)
            | Q(encargado__icontains=query)
            | Q(descripcion__icontains=query)
        )
    return render(request, 'departamentos/gestion_lista.html', {
        'departamentos': departamentos,
        'query': query,
    })


@permission_required('departamentosApp.add_departamento', raise_exception=True)
def gestion_crear(request):
    form = DepartamentoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'El departamento se creó correctamente.')
        return redirect('departamentos_gestion_lista')
    return render(request, 'departamentos/formulario.html', {
        'form': form,
        'titulo': 'Crear departamento',
        'cancel_url': 'departamentos_gestion_lista',
    })


@permission_required('departamentosApp.change_departamento', raise_exception=True)
def gestion_editar(request, pk):
    departamento = get_object_or_404(Departamento, pk=pk)
    form = DepartamentoForm(request.POST or None, instance=departamento)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'El departamento se actualizó correctamente.')
        return redirect('departamentos_gestion_lista')
    return render(request, 'departamentos/formulario.html', {
        'form': form,
        'titulo': 'Editar departamento',
        'cancel_url': 'departamentos_gestion_lista',
    })


@permission_required('departamentosApp.delete_departamento', raise_exception=True)
def gestion_eliminar(request, pk):
    departamento = get_object_or_404(Departamento, pk=pk)
    if request.method == 'POST':
        departamento.delete()
        messages.success(request, 'El departamento se eliminó correctamente.')
        return redirect('departamentos_gestion_lista')
    return render(request, 'mantenedores/confirmar_eliminacion.html', {
        'objeto': departamento,
        'titulo': 'Eliminar departamento',
        'cancel_url': 'departamentos_gestion_lista',
    })