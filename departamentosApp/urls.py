from django.urls import path
from departamentosApp import views as vdep

urlpatterns = [
    path('', vdep.inicio, name='departamentos_inicio'),
    path('listado/', vdep.listado, name='departamentos_listado'),
    path('detalle/<int:departamento_id>/', vdep.detalle, name='departamentos_detalle'),
]