from django.urls import path
from departamentosApp import views as vdep

urlpatterns = [
    path('', vdep.inicio, name='departamentos_inicio'),
    path('listado/', vdep.listado, name='departamentos_listado'),
    path('detalle/<int:departamento_id>/', vdep.detalle, name='departamentos_detalle'),
    path('gestion/', vdep.gestion_lista, name='departamentos_gestion_lista'),
    path('gestion/nuevo/', vdep.gestion_crear, name='departamentos_gestion_crear'),
    path('gestion/<int:pk>/editar/', vdep.gestion_editar, name='departamentos_gestion_editar'),
    path('gestion/<int:pk>/eliminar/', vdep.gestion_eliminar, name='departamentos_gestion_eliminar'),
]