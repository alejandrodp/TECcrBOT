import click

from tcrb.cli.commands.bot import bot
from tcrb.cli.commands.database import db
from tcrb.cli.commands.scraper import scraper


@click.group()
def cli():
    """
    tcli - teccrbot command line interface

    Esta es una utilidad de linea de comandos para manejar el servidor y otros
    aspectos del software que constituye a teccrbot y a sus utilidades
    relacionadas.
    """
    pass


cli.add_command(bot)
cli.add_command(db)
cli.add_command(scraper)


if __name__ == '__main__':
    cli()
