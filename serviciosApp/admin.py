from django.contrib import admin

from .models import Servicio


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'plazo_dias', 'gratuito', 'estado')
    list_filter = ('categoria', 'gratuito', 'estado')
    search_fields = ('nombre', 'categoria', 'descripcion')
    ordering = ('categoria', 'nombre')
