import click

from .backend.bot import start_bot, check_database

import os
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tcrb.settings")
application = get_wsgi_application()

@click.group()
def bot():
    """
    Manejar el servidor del bot
    """
    pass


@bot.command("start")
def start():
    """
    Inicia el bot con la configuración por defecto.
    """
    click.echo("Iniciando bot...")

    click.secho(message="Revisando migraciones...", nl=False)
    if check_database():
        click.secho(message=" Ok", fg='green')
    else:
        click.secho(message="WARNING", fg='yellow')
        click.echo("\tBase de datos parece no estar inicializada.")

    start_bot()