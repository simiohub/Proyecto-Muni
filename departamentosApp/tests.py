from django.test import TestCase

from departamentosApp.models import Departamento


class DepartamentoModelTests(TestCase):
    def test_crear_departamento_y_filtrar_por_prioridad(self):
        Departamento.objects.create(
            nombre='Departamento de Pruebas',
            encargado='Ana López',
            horario='08:30 - 17:00',
            telefono='+56 51 222 0009',
            descripcion='Departamento de ejemplo para pruebas.',
            prioridad='alta',
        )

        self.assertEqual(Departamento.objects.count(), 1)
        self.assertEqual(
            list(Departamento.objects.filter(prioridad='alta').values_list('nombre', flat=True)),
            ['Departamento de Pruebas'],
        )
