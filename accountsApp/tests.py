from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from urllib.parse import urlparse

from accountsApp.roles import ADMINISTRADOR, ADMINISTRATIVO

User = get_user_model()


class AccountFlowTests(TestCase):
    def setUp(self):
        self.admin_group, _ = Group.objects.get_or_create(name=ADMINISTRADOR)
        self.admin = User.objects.create_user(
            username='admin-pruebas',
            password='ClaveSegura123!',
            email='admin@example.com',
        )
        self.admin.groups.add(self.admin_group)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('accounts:dashboard'))

        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('accounts:dashboard')}",
        )

    def test_django_admin_route_is_disabled(self):
        response = self.client.get('/admin/')

        self.assertEqual(response.status_code, 404)

    def test_user_without_role_cannot_open_dashboard(self):
        account = User.objects.create_user(
            username='sin-perfil',
            password='ClaveSegura123!',
        )
        self.client.force_login(account)

        response = self.client.get(reverse('accounts:dashboard'))

        self.assertEqual(response.status_code, 403)

    def test_admin_can_create_user_with_selected_group(self):
        self.client.force_login(self.admin)
        Group.objects.get_or_create(name=ADMINISTRATIVO)

        response = self.client.post(reverse('accounts:user_create'), {
            'username': 'personal',
            'email': 'personal@example.com',
            'first_name': 'Personal',
            'last_name': 'Municipal',
            'role': ADMINISTRATIVO,
            'password1': 'ClaveSegura123!Otra',
            'password2': 'ClaveSegura123!Otra',
        })

        self.assertRedirects(response, reverse('accounts:user_list'))
        account = User.objects.get(username='personal')
        self.assertTrue(account.groups.filter(name=ADMINISTRATIVO).exists())

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_password_reset_sends_recovery_link(self):
        response = self.client.post(reverse('accounts:password_reset'), {
            'email': self.admin.email,
        })

        self.assertRedirects(response, reverse('accounts:password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)
        reset_url = next(
            line for line in mail.outbox[0].body.splitlines()
            if line.startswith('http://') or line.startswith('https://')
        )
        response = self.client.get(urlparse(reset_url).path)
        self.assertEqual(response.status_code, 302)

        reset_path = response.url
        response = self.client.get(reset_path)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reset_path, {
            'new_password1': 'NuevaClaveSegura456!',
            'new_password2': 'NuevaClaveSegura456!',
        })

        self.assertRedirects(
            response,
            reverse('accounts:password_reset_complete'),
        )
        self.admin.refresh_from_db()
        self.assertTrue(self.admin.check_password('NuevaClaveSegura456!'))