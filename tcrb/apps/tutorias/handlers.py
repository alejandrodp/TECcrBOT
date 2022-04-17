from telegram.ext import CallbackContext


def main_menu_handler(reply, context: CallbackContext) -> None:
    response = "Las tutorías aún no se encuentran disponibles en este bot." \
               "Pero puede obtener más información en el siguiente grupo de telegram: " \
               "https://t.me/Tutorias_ExitoAcademicoTEC"

    reply.text(response)
