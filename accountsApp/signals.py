from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .roles import ADMINISTRADOR, ADMINISTRATIVO, ROLE_NAMES, SUPERVISOR


@receiver(post_migrate)
def create_role_groups(sender, **kwargs):
	if sender.label not in {'accountsApp', 'departamentosApp', 'serviciosApp'}:
		return

	groups = {
		name: Group.objects.get_or_create(name=name)[0]
		for name in ROLE_NAMES
	}
	all_permissions = Permission.objects.all()
	groups[ADMINISTRADOR].permissions.set(all_permissions)

	app_permissions = Permission.objects.filter(
		content_type__app_label__in=('departamentosApp', 'serviciosApp'),
	)
	service_request_permissions = app_permissions.filter(
		content_type__model='solicitudservicio',
	)
	app_permissions = app_permissions.exclude(
		content_type__model='solicitudservicio',
	)
	supervisor_permissions = app_permissions.filter(
		codename__regex=r'^(add|change|view)_',
	) | service_request_permissions.filter(
		codename__regex=r'^(add|change|view)_',
	)
	groups[SUPERVISOR].permissions.set(supervisor_permissions)

	administrative_permissions = app_permissions.filter(
		codename__regex=r'^(view)_',
	) | service_request_permissions.filter(
		codename__regex=r'^(add|view)_',
	)
	groups[ADMINISTRATIVO].permissions.set(administrative_permissions)