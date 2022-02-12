from telegram import InlineKeyboardButton as IKB
from telegram.ext import CallbackContext

from tcrb.core import BotAppConfig
from tcrb.common.util import Reply
from . import apps

config = BotAppConfig(apps.TransportationConfig.name, apps.TransportationConfig.verbose_name)


def menu_entry(reply: Reply, context: CallbackContext) -> None:
    response = "(Última modificación: 06-02-2022)\n\n" \
               "El servicio de bus del TEC no se encuentra disponible en este momento, " \
               "solo se está ofreciendo el siguiente servicio:\n\n" \
               "Servicio de buseta que sale del centro de Cartago hacia el TEC a las 7:20 a.m\n" \
               "Servicio de buseta que sale del TEC al centro de Cartago a las 4:40 p.m\n\n" \
               "Fuente: FEITEC"

    reply.text(response)
