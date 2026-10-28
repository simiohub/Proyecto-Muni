from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

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


class DepartamentoCrudTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username='admin-departamentos',
            email='admin-departamentos@example.com',
            password='ClaveSegura123!',
        )
        self.client.force_login(self.admin)

    def test_departamento_crud_and_search(self):
        create_url = reverse('departamentos_gestion_crear')
        response = self.client.post(create_url, {
            'nombre': 'Dirección de Aseo',
            'encargado': 'Patricia Soto',
            'horario': '09:00 - 17:00',
            'telefono': '+56 51 222 1000',
            'descripcion': 'Mantención comunal.',
            'prioridad': 'alta',
        })
        self.assertRedirects(response, reverse('departamentos_gestion_lista'))

        departamento = Departamento.objects.get(nombre='Dirección de Aseo')
        response = self.client.get(reverse('departamentos_gestion_lista'), {'q': 'Patricia'})
        self.assertContains(response, 'Dirección de Aseo')

        response = self.client.post(
            reverse('departamentos_gestion_editar', args=[departamento.pk]),
            {
                'nombre': 'Dirección de Aseo y Ornato',
                'encargado': 'Patricia Soto',
                'horario': '09:00 - 17:00',
                'telefono': '+56 51 222 1000',
                'descripcion': 'Mantención comunal.',
                'prioridad': 'media',
            },
        )
        self.assertRedirects(response, reverse('departamentos_gestion_lista'))
        departamento.refresh_from_db()
        self.assertEqual(departamento.nombre, 'Dirección de Aseo y Ornato')

        delete_url = reverse('departamentos_gestion_eliminar', args=[departamento.pk])
        self.assertEqual(self.client.get(delete_url).status_code, 200)
        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse('departamentos_gestion_lista'))
        self.assertFalse(Departamento.objects.exists())
