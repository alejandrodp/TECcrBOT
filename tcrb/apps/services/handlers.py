from telegram.ext import CallbackContext


def main_menu_handler(reply, context: CallbackContext) -> None:
    response = "Puede buscar servicios escribiendo su nombre.\n\n " \
               "Actualmente puede encontrar servicios de becas, " \
               "bibliotecarios, matrícula, servicios médicos o del DOP, entre otros.\n\n" \
               "Ejemplos: becas, libro beca, emergencias, pscologia"

    reply.text(response)
