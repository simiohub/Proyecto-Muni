from django.db import models
from django.conf import settings


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


class SolicitudServicio(models.Model):
    ESTADO_CHOICES = [
        ('recibida', 'Recibida'),
        ('en_revision', 'En revisión'),
        ('resuelta', 'Resuelta'),
        ('rechazada', 'Rechazada'),
    ]

    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='solicitudes_servicio',
    )
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.PROTECT,
        related_name='solicitudes',
    )
    motivo = models.TextField()
    direccion = models.CharField(max_length=250)
    telefono_contacto = models.CharField(max_length=50)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='recibida',
    )
    creada_en = models.DateTimeField(auto_now_add=True)
    actualizada_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creada_en']
        verbose_name = 'Solicitud de servicio'
        verbose_name_plural = 'Solicitudes de servicio'

    def __str__(self):
        return f'Solicitud #{self.pk} - {self.servicio.nombre}'
