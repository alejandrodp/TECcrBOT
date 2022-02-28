<h1 align="center">TECcrBOT</h1>

!["banner"](banner.jpg)

# Descripción
TECcrBot (TCRB) es un bot de [Telegram](https://telegram.org/) dedicado a proporcionar información y utilidades a los integrantes de la comunidad del ITCR.

Creado por Esteban Sánchez Trejos, quién en conjunto con la asociación de estudiantes de la carrera de mecatrónica lo desarrolló durante 2017-2021. 

Actualmente [Cluster451](https://cluster451.org/) mantiene el proyecto.

# Instrucciones para correr el proyecto


## Prerequisitos
---
0. Tener python instalado en el sistema
   - El proyecto ha sido probado en la versión 3.9, no se garantiza funcionalidad con otras versiones.
<br></br> 

1. Descargar e instalar modulos en requirements.txt.
   - Se recomienda instalar los modulos con `pip install -r requirements.txt` dentro de un [entorno virtual](https://docs.python.org/3/tutorial/venv.html).
<br></br>

1. Crear un archivo llamado .env en la carpeta raíz con las siguientes variables:

   - `SECRET_KEY`: Esta es la llave de django para funcionamiento interno del mismo, puede generarse con este código: `python -c 'from django.core.management.utils import  get_random_secret_key; print(get_random_secret_key())'`
   - `BOT_SECRET_KEY`: Este es el token de telegram sacado de [BotFather](https://t.me/botfather).
   - `DATABASE_URL`: Esta es la url de la BD a utilizar, para utilizar la incluída en este repo pueden usar esta: `sqlite:///./tcrb.sqlite3`
   - `DEBUG`: Especificar como verdadero durante desarrollo. Falso indica modo de producción (*prod*). **Aún no están las configuraciones necesarias para habilitar *prod*, por lo tanto mantener similar al ejemplo de abajo.**
   <br></br> 

    Al final, el archivo se debería ver parecido a esto:

    ```
    SECRET_KEY=secret
    BOT_SECRET_KEY=secret
    DATABASE_URL=sqlite:///./tcrb.sqlite3
    DEBUG=true
    ```
## Correr el bot
- Ejecutar el siguiente comando desde la carpeta raíz del proyecto: `./manage.py start_bot`.

