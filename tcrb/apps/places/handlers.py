from telegram.ext import CallbackContext


def main_menu_handler(reply, context: CallbackContext) -> None:
    response = "Puede buscar ubicaciones escribiendo el nombre del lugar. Obtendrá detalles " \
               "como la ubicación geográfica, descripción e imagen.\n\n" \
               "Ejemplos: A1, D3, pretil, restaurantes"

    reply.text(response)
