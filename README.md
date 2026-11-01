# Portal Municipal

Aplicación web para consultar departamentos y servicios municipales, gestionar solicitudes y administrar usuarios por perfil.

## Iniciar en EC2

Conéctate por SSH y ejecuta:

```bash
cd /var/www/proyectomuni
source venv/bin/activate
python manage.py migrate
sudo systemctl restart gunicorn
sudo systemctl status gunicorn --no-pager
```

Si aparece `active (running)`, abre en el navegador la IP pública de la instancia.

## Demostración

1. Consultar departamentos y servicios.
2. Iniciar y cerrar sesión.
3. Mostrar los paneles de Administrador, Supervisor y Administrativo.
4. Crear una solicitud como Administrativo y cambiar su estado como Supervisor.
5. Mostrar la búsqueda y el CRUD de departamentos o servicios.
6. Probar la recuperación de contraseña y confirmar el correo.

La aplicación se administra desde sus propias páginas; no se utiliza Django Admin.
