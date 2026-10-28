from django.apps import AppConfig


class AccountsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accountsApp'

    def ready(self):
        from . import signals