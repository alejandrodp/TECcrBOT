import click

from .backend.bot import start_bot, check_database
from .database import makemigrations, migrate, populate, index

@click.group()
def bot():
    """
    Manejar el servidor del bot
    """
    pass


@bot.command("start")
@click.option("--builddb", show_default=True, default=False, is_flag=True,
                                help="Crea las migraciones, \
                                migra, popula la base de datos \
                                y genera el índice antes de iniciar.")
def start(builddb):
    """
    Inicia el bot con la configuración por defecto.
    """
    if builddb:
        makemigrations()
        migrate()
        populate()
        index()
    
    click.echo("Iniciando bot...")

    click.secho(message="Revisando base de datos...", nl=False)
    if check_database():
        click.secho(message=" Ok", fg='green')
    else:
        click.secho(message=" WARNING", fg='yellow')
        click.echo("\tBase de datos parece no estar inicializada.")

    if start_bot():
        click.secho(message="Bot iniciado", fg='green')
    else:
        click.secho(message="Error al iniciar bot", fg='red')


