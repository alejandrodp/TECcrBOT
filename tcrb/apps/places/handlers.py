from telegram.ext import CallbackContext

from tcrb.apps.config.handlers.base import Reply


def main_menu_handler(reply: Reply, context: CallbackContext) -> None:
    response = "Puede buscar lugares escribiendo el nombre " \
               "para obtener detalles como la ubicación geográfica, descripción e imagen.\n" \
               "Algunos ejemplos de consultas que puede realizar son: A1, D3, pretil, restaurantes, entre otros."

    reply.text(response)
