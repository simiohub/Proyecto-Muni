from django.db import models


class Departamento(models.Model):
    PRIORIDAD_CHOICES = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]

    nombre = models.CharField(max_length=200)
    encargado = models.CharField(max_length=200)
    horario = models.CharField(max_length=100)
    telefono = models.CharField(max_length=50)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='media')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return self.nombre
