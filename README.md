# tcrb-dev
Repo temporal para TCRB

# Instrucciones para correr el proyecto

0. Descargar e instalar el requirements.txt.

1. Crear un archivo llamado .env en la carpeta raíz con las siguientes variables:

- `SECRET_KEY`: Esta es la llave de django para funcionamiento interno del mismo, puede generarse con este código: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
- `BOT_SECRET_KEY`: Este es el token de telegram sacado de @BotFather.
- `DATABASE_URL`: Esta es la url de la BD a utilizar, para utilizar la incluída en este repo pueden usar esta: `sqlite:///./tcrb.sqlite3`
- `DEBUG`: Esta es una flag para indicar si se está en prod o no, aún no están las configuraciones necesarias para mantener en prod, entonces mantengan esta flag en verdadero.

2. Ejecutar el siguiente comando desde la carpeta raíz inicia el bot: `./manage.py start_bot`.
