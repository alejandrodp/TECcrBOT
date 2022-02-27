from telegram import InlineKeyboardButton as IKB
from telegram.ext import CallbackContext

from tcrb.common.util import Reply


def main_entry(reply: Reply, context: CallbackContext) -> None:
    response = "Para buscar servicios escriba el nombre, " \
               "actualmente puede encontrar servicios de becas, " \
               "bibliotecarios, matrícula, servicios médicos o del DOP, entre otros.\n\n" \
               "Ejemplos de las consultas que puede realizar son: becas, libro beca, emergencias, pscologia"

    reply.text(response)
