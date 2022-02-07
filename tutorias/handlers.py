from telegram.ext import CallbackContext

from common.util import Reply
from tcrb.core import BotAppConfig
from tutorias import apps

config = BotAppConfig(apps.TutoriasConfig.name, apps.TutoriasConfig.verbose_name)


def main_menu_handler(reply: Reply, context: CallbackContext) -> None:

    response = "Las tutorías aún no se encuentran disponibles en este bot. " \
               "Se estarán mostrando en este apartado en cuanto estén disponibles.\n" \
               "Para cualquier duda comunicarse con el departamento de orientación y psicología (DOP)"

    reply.text(response)
