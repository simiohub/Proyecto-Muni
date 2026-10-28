from functools import wraps

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from departamentosApp.models import Departamento
from serviciosApp.models import Servicio

from .forms import UserAccountCreationForm
from .roles import ADMINISTRADOR, ADMINISTRATIVO, SUPERVISOR

User = get_user_model()


def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped(request, *args, **kwargs):
            if request.user.is_superuser or request.user.groups.filter(
                name__in=allowed_roles,
            ).exists():
                return view_func(request, *args, **kwargs)
            raise PermissionDenied

        return wrapped

    return decorator


def dashboard(request):
    groups = set(request.user.groups.values_list('name', flat=True))
    if request.user.is_superuser or ADMINISTRADOR in groups:
        role = ADMINISTRADOR
    elif SUPERVISOR in groups:
        role = SUPERVISOR
    elif ADMINISTRATIVO in groups:
        role = ADMINISTRATIVO
    else:
        raise PermissionDenied

    return render(request, 'accounts/dashboard.html', {
        'role': role,
        'department_count': Departamento.objects.count(),
        'service_count': Servicio.objects.count(),
    })


@role_required(ADMINISTRADOR)
def user_list(request):
    users = User.objects.prefetch_related('groups').order_by('username')
    return render(request, 'accounts/user_list.html', {'users': users})


@role_required(ADMINISTRADOR)
def user_create(request):
    form = UserAccountCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'La cuenta se creó correctamente.')
        return redirect('accounts:user_list')

    return render(request, 'accounts/user_form.html', {'form': form})


class PortalLoginView(LoginView):
    template_name = 'accounts/login.html'


class PortalLogoutView(LogoutView):
    http_method_names = ['post', 'options']


class PortalPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.txt'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')


class PortalPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PortalPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class PortalPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'