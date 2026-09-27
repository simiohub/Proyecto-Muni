from django.test import TestCase

from serviciosApp.models import Servicio


class ServicioModelTests(TestCase):
    def test_crear_servicio_y_filtrar_por_categoria(self):
        Servicio.objects.create(
            nombre='Tramite de prueba',
            categoria='Trámite',
            descripcion='Servicio de ejemplo para pruebas.',
            plazo_dias=2,
            gratuito=False,
            estado='disponible',
        )

        self.assertEqual(Servicio.objects.count(), 1)
        self.assertEqual(
            list(Servicio.objects.filter(categoria='Trámite').values_list('nombre', flat=True)),
            ['Tramite de prueba'],
        )
