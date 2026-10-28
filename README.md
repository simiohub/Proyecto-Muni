# Proyecto-Muni

Aplicacion Django para consultar departamentos y servicios municipales.

## Configuracion local

1. Crea y activa un entorno virtual.
2. Instala las dependencias con `pip install -r requirements.txt`.
3. Copia `.env.example` como `.env` y completa `DB_PASSWORD`.
4. Genera una clave Django y reemplaza `DJANGO_SECRET_KEY` en `.env`:

   ```powershell
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. Ejecuta `python manage.py migrate` y luego `python manage.py runserver`.

No subas `.env` ni compartas sus valores. `.env.example` contiene solo nombres de variables y valores de muestra.

## Evaluación sumativa 3

La gestión se realiza desde páginas propias con Django Templates y Bootstrap. Django Admin está deshabilitado y no forma parte del flujo.

Después de configurar la base relacional en `.env`, aplica migraciones y crea la primera cuenta con:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

El primer superusuario puede iniciar sesión en `/cuentas/ingresar/` y crear cuentas asignadas a los perfiles Administrador, Supervisor o Administrativo. Los grupos y permisos se generan al aplicar migraciones.

Rutas de demostración:

- `/cuentas/ingresar/`: inicio y cierre de sesión.
- `/cuentas/panel/`: dashboard diferenciado por perfil.
- `/cuentas/usuarios/`: gestión de cuentas, solo Administrador.
- `/departamentos/gestion/`: mantenedor CRUD de departamentos.
- `/servicios/gestion/`: mantenedor CRUD de servicios.
- `/servicios/solicitudes/`: solicitudes de servicio y seguimiento de estado.
- `/cuentas/recuperar/`: recuperación de contraseña mediante token.

En desarrollo, el correo de recuperación se escribe en la consola mediante `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend`. Para demostrar el envío real, configura un proveedor SMTP en las variables `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS` y `DEFAULT_FROM_EMAIL`. No agregues credenciales al repositorio.

Para desplegar en EC2, configura `DJANGO_DEBUG=false`, `DJANGO_ALLOWED_HOSTS` con el dominio o IP pública y las variables de conexión MySQL correspondientes en el entorno del servidor. Luego ejecuta `python manage.py migrate` y recopila estáticos con `python manage.py collectstatic`.

La evidencia resumida de apoyo de IA y su aplicación se encuentra en [`docs/evidencia-ia.md`](docs/evidencia-ia.md). Añade al documento técnico las capturas requeridas de prompts, respuestas, interfaces, AWS y GitHub.
