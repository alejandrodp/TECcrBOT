import click

from .backend.database import make_migrations_db, migrate_db, populate_db, index_db

@click.group()
def db():
    """
    Manejar la base de datos del bot
    """
    pass


@db.command("makemigrations")
def makemigrations():
    """
    Genera las migraciones.
    """
    click.secho(message="Generando migraciones...", nl=False)
    if make_migrations_db():
        click.secho(message=" Ok", fg="green")
    else:
        click.secho(message=" WARNING", fg="yellow")
        click.echo("\tError al generar migraciones.")


@db.command("migrate")
def migrate():
    """
    Ejecuta las migraciones.
    """
    click.secho(message="Migrando...", nl=False)
    if migrate_db():
        click.secho(message=" Ok", fg="green")
    else:
        click.secho(message=" WARNING", fg="yellow")
        click.echo("\tError al migrar.")


@db.command("populate")
def populate():
    """
    Popula la base de datos.
    """
    click.secho(message="Populando base de datos...", nl=False)
    if populate_db():
        click.secho(message=" Ok", fg="green")
    else:
        click.secho(message=" WARNING", fg="yellow")
        click.echo("\tError al popular la base de datos.")


@db.command("index")
def index():
    """
    Genera el índice.
    """
    click.secho(message="Indexando...", nl=False)
    if index_db():
        click.secho(message=" Ok", fg="green")
    else:
        click.secho(message=" WARNING", fg="yellow")
        click.echo("\tError al indexar.")
