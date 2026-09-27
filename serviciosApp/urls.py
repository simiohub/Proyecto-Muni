from django.urls import path
from serviciosApp import views as vser

urlpatterns = [
    path('', vser.inicio, name='servicios_inicio'),
    path('listado/', vser.listado, name='servicios_listado'),
]