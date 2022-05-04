import click


@click.group()
def db():
    """
    Manejar la base de datos del bot
    """
    pass


@db.command("start")
def start():
    """
    Inicia la db con la configuración por defecto.
    """
    click.echo("Iniciando db...")