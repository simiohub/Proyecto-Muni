from django.urls import path
from serviciosApp import views as vser

urlpatterns = [
    path('', vser.inicio, name='servicios_inicio'),
    path('listado/', vser.listado, name='servicios_listado'),
    path('gestion/', vser.gestion_lista, name='servicios_gestion_lista'),
    path('gestion/nuevo/', vser.gestion_crear, name='servicios_gestion_crear'),
    path('gestion/<int:pk>/editar/', vser.gestion_editar, name='servicios_gestion_editar'),
    path('gestion/<int:pk>/eliminar/', vser.gestion_eliminar, name='servicios_gestion_eliminar'),
    path('solicitudes/', vser.solicitudes_lista, name='solicitudes_lista'),
    path('solicitudes/nueva/', vser.solicitud_crear, name='solicitud_crear'),
    path('solicitudes/<int:pk>/', vser.solicitud_detalle, name='solicitud_detalle'),
    path('solicitudes/<int:pk>/estado/', vser.solicitud_actualizar_estado, name='solicitud_actualizar_estado'),
]