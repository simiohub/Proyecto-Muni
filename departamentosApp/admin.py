from django.contrib import admin

from .models import Departamento


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'encargado', 'prioridad', 'telefono')
    list_filter = ('prioridad',)
    search_fields = ('nombre', 'encargado', 'descripcion')
    ordering = ('nombre',)
