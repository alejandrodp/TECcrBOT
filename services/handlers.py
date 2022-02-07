from telegram import InlineKeyboardButton
from telegram.ext import CallbackContext

from common.util import Reply

IKB = InlineKeyboardButton


def main_entry(reply: Reply, context: CallbackContext) -> None:
    response = "Para buscar servicios escriba el nombre, " \
               "actualmente puede encontrar servicios de becas, " \
               "bibliotecarios, matrícula, servicios médicos o del DOP, entre otros.\n\n" \
               "Ejemplos de las consultas que puede realizar son: becas, libro beca, emergencias, pscologia"

    reply.text(response)
