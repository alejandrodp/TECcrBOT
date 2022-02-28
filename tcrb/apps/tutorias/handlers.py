from telegram.ext import CallbackContext


def main_menu_handler(reply, context: CallbackContext) -> None:
    response = "Las tutorías aún no se encuentran disponibles en este bot.\n" \
               "Se estarán mostrando en este apartado en cuanto estén disponibles.\n\n" \
               "Para cualquier duda comunicarse con el departamento de orientación y psicología (DOP)"

    reply.text(response)
