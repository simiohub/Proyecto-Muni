from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('ingresar/', views.PortalLoginView.as_view(), name='login'),
    path('salir/', views.PortalLogoutView.as_view(), name='logout'),
    path('panel/', login_required(views.dashboard), name='dashboard'),
    path('usuarios/', views.user_list, name='user_list'),
    path('usuarios/nuevo/', views.user_create, name='user_create'),
    path(
        'recuperar/',
        views.PortalPasswordResetView.as_view(),
        name='password_reset',
    ),
    path(
        'recuperar/listo/',
        views.PortalPasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        'recuperar/<uidb64>/<token>/',
        views.PortalPasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'recuperar/completado/',
        views.PortalPasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
]