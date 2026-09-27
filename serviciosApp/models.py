from django.db import models


class Servicio(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('con restricciones', 'Con restricciones'),
        ('no disponible', 'No disponible'),
    ]

    nombre = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    descripcion = models.TextField()
    plazo_dias = models.PositiveIntegerField(default=1)
    gratuito = models.BooleanField(default=True)
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='disponible')

    class Meta:
        ordering = ['categoria', 'nombre']
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return self.nombre
