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
