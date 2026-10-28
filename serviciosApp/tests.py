from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from serviciosApp.models import Servicio, SolicitudServicio
from accountsApp.roles import ADMINISTRADOR, ADMINISTRATIVO, SUPERVISOR


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


class ServicioCrudTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username='admin-servicios',
            email='admin-servicios@example.com',
            password='ClaveSegura123!',
        )
        self.client.force_login(self.admin)

    def test_servicio_crud_and_search(self):
        create_url = reverse('servicios_gestion_crear')
        response = self.client.post(create_url, {
            'nombre': 'Permiso de circulación',
            'categoria': 'Tránsito',
            'descripcion': 'Renovación anual.',
            'plazo_dias': 3,
            'gratuito': False,
            'estado': 'disponible',
        })
        self.assertRedirects(response, reverse('servicios_gestion_lista'))

        servicio = Servicio.objects.get(nombre='Permiso de circulación')
        response = self.client.get(reverse('servicios_gestion_lista'), {'q': 'Tránsito'})
        self.assertContains(response, 'Permiso de circulación')

        response = self.client.post(
            reverse('servicios_gestion_editar', args=[servicio.pk]),
            {
                'nombre': 'Permiso de circulación municipal',
                'categoria': 'Tránsito',
                'descripcion': 'Renovación anual.',
                'plazo_dias': 4,
                'gratuito': False,
                'estado': 'disponible',
            },
        )
        self.assertRedirects(response, reverse('servicios_gestion_lista'))
        servicio.refresh_from_db()
        self.assertEqual(servicio.nombre, 'Permiso de circulación municipal')

        delete_url = reverse('servicios_gestion_eliminar', args=[servicio.pk])
        self.assertEqual(self.client.get(delete_url).status_code, 200)
        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse('servicios_gestion_lista'))
        self.assertFalse(Servicio.objects.exists())


class SolicitudServicioTests(TestCase):
    def setUp(self):
        self.administrative_group, _ = Group.objects.get_or_create(
            name=ADMINISTRATIVO,
        )
        self.supervisor_group, _ = Group.objects.get_or_create(name=SUPERVISOR)
        self.solicitante = get_user_model().objects.create_user(
            username='funcionario',
            password='ClaveSegura123!',
        )
        self.solicitante.groups.add(self.administrative_group)
        self.supervisor = get_user_model().objects.create_user(
            username='supervisor',
            password='ClaveSegura123!',
        )
        self.supervisor.groups.add(self.supervisor_group)
        self.servicio = Servicio.objects.create(
            nombre='Retiro de residuos voluminosos',
            categoria='Aseo',
            descripcion='Solicitud de retiro domiciliario.',
            plazo_dias=5,
            estado='disponible',
        )

    def test_administrativo_creates_and_only_sees_own_request(self):
        other_user = get_user_model().objects.create_user(username='otra-persona')
        other_request = SolicitudServicio.objects.create(
            solicitante=other_user,
            servicio=self.servicio,
            motivo='Solicitud privada de prueba.',
            direccion='Calle Uno 123',
            telefono_contacto='+56 9 1111 2222',
        )
        self.client.force_login(self.solicitante)
        response = self.client.post(reverse('solicitud_crear'), {
            'servicio': self.servicio.pk,
            'motivo': 'Solicito retiro de un mueble.',
            'direccion': 'Calle Dos 456',
            'telefono_contacto': '+56 9 3333 4444',
        })

        solicitud = SolicitudServicio.objects.get(solicitante=self.solicitante)
        self.assertRedirects(
            response,
            reverse('solicitud_detalle', args=[solicitud.pk]),
        )
        self.assertEqual(solicitud.estado, 'recibida')
        response = self.client.get(reverse('solicitudes_lista'))
        self.assertContains(response, f'#{solicitud.pk}')
        self.assertNotContains(response, f'#{other_request.pk}')
        self.assertEqual(
            self.client.post(
                reverse('solicitud_actualizar_estado', args=[solicitud.pk]),
                {'estado': 'resuelta'},
            ).status_code,
            403,
        )

    def test_supervisor_can_update_request_status(self):
        solicitud = SolicitudServicio.objects.create(
            solicitante=self.solicitante,
            servicio=self.servicio,
            motivo='Solicitud de actualización de estado.',
            direccion='Avenida Central 789',
            telefono_contacto='+56 9 5555 6666',
        )
        self.client.force_login(self.supervisor)

        response = self.client.post(
            reverse('solicitud_actualizar_estado', args=[solicitud.pk]),
            {'estado': 'en_revision'},
        )

        self.assertRedirects(
            response,
            reverse('solicitud_detalle', args=[solicitud.pk]),
        )
        solicitud.refresh_from_db()
        self.assertEqual(solicitud.estado, 'en_revision')
