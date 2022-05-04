import click


@click.group()
def scraper():
    """
    Manejar los scrapers que generan información para el bot
    """
    pass


@scraper.command("scrap")
def scrap():
    click.echo("Iniciando scrap...")