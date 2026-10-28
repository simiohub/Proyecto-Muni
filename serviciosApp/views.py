from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from .forms import EstadoSolicitudForm, ServicioForm, SolicitudServicioForm
from .models import Servicio, SolicitudServicio


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


@permission_required('serviciosApp.view_servicio', raise_exception=True)
def gestion_lista(request):
    query = request.GET.get('q', '').strip()
    servicios = Servicio.objects.all()
    if query:
        servicios = servicios.filter(
            Q(nombre__icontains=query)
            | Q(categoria__icontains=query)
            | Q(descripcion__icontains=query)
        )
    return render(request, 'servicios/gestion_lista.html', {
        'servicios': servicios,
        'query': query,
    })


@permission_required('serviciosApp.add_servicio', raise_exception=True)
def gestion_crear(request):
    form = ServicioForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'El servicio se creó correctamente.')
        return redirect('servicios_gestion_lista')
    return render(request, 'mantenedores/formulario.html', {
        'form': form,
        'titulo': 'Crear servicio',
        'cancel_url': 'servicios_gestion_lista',
    })


@permission_required('serviciosApp.change_servicio', raise_exception=True)
def gestion_editar(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    form = ServicioForm(request.POST or None, instance=servicio)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'El servicio se actualizó correctamente.')
        return redirect('servicios_gestion_lista')
    return render(request, 'mantenedores/formulario.html', {
        'form': form,
        'titulo': 'Editar servicio',
        'cancel_url': 'servicios_gestion_lista',
    })


@permission_required('serviciosApp.delete_servicio', raise_exception=True)
def gestion_eliminar(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        servicio.delete()
        messages.success(request, 'El servicio se eliminó correctamente.')
        return redirect('servicios_gestion_lista')
    return render(request, 'mantenedores/confirmar_eliminacion.html', {
        'objeto': servicio,
        'titulo': 'Eliminar servicio',
        'cancel_url': 'servicios_gestion_lista',
    })


@permission_required('serviciosApp.view_solicitudservicio', raise_exception=True)
def solicitudes_lista(request):
    solicitudes = SolicitudServicio.objects.select_related('servicio', 'solicitante')
    if not request.user.has_perm('serviciosApp.change_solicitudservicio'):
        solicitudes = solicitudes.filter(solicitante=request.user)

    estado = request.GET.get('estado', '')
    query = request.GET.get('q', '').strip()
    if estado:
        solicitudes = solicitudes.filter(estado=estado)
    if query:
        solicitudes = solicitudes.filter(
            Q(servicio__nombre__icontains=query)
            | Q(motivo__icontains=query)
            | Q(solicitante__username__icontains=query)
        )
    return render(request, 'servicios/solicitudes_lista.html', {
        'solicitudes': solicitudes,
        'estado': estado,
        'estados': SolicitudServicio.ESTADO_CHOICES,
        'query': query,
        'puede_cambiar': request.user.has_perm(
            'serviciosApp.change_solicitudservicio',
        ),
    })


@permission_required('serviciosApp.add_solicitudservicio', raise_exception=True)
def solicitud_crear(request):
    form = SolicitudServicioForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        solicitud = form.save(commit=False)
        solicitud.solicitante = request.user
        solicitud.save()
        messages.success(request, 'La solicitud se registró correctamente.')
        return redirect('solicitud_detalle', pk=solicitud.pk)
    return render(request, 'servicios/solicitud_form.html', {'form': form})


@permission_required('serviciosApp.view_solicitudservicio', raise_exception=True)
def solicitud_detalle(request, pk):
    solicitud = get_object_or_404(
        SolicitudServicio.objects.select_related('servicio', 'solicitante'),
        pk=pk,
    )
    if (
        solicitud.solicitante_id != request.user.pk
        and not request.user.has_perm('serviciosApp.change_solicitudservicio')
    ):
        raise PermissionDenied
    return render(request, 'servicios/solicitud_detalle.html', {
        'solicitud': solicitud,
        'form': EstadoSolicitudForm(initial={'estado': solicitud.estado}),
        'puede_cambiar': request.user.has_perm(
            'serviciosApp.change_solicitudservicio',
        ),
    })


@permission_required('serviciosApp.change_solicitudservicio', raise_exception=True)
def solicitud_actualizar_estado(request, pk):
    solicitud = get_object_or_404(SolicitudServicio, pk=pk)
    form = EstadoSolicitudForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        solicitud.estado = form.cleaned_data['estado']
        solicitud.save(update_fields=['estado', 'actualizada_en'])
        messages.success(request, 'El estado de la solicitud se actualizó.')
    else:
        messages.error(request, 'Selecciona un estado válido.')
    return redirect('solicitud_detalle', pk=solicitud.pk)