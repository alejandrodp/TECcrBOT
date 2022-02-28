import re

from telegram.ext import Filters

from tcrb.apps.config.handlers import HandlerConfig, MessageHandler
from tcrb.apps.transportation.handlers import main_menu_handler

TRANSPORTATION_DESC = "Servicios de transporte \U0001f68c"


TRANSPORTATION_HANDLERS = HandlerConfig([
    # TODO: Eliminar esto cuando se restauren los buses
    MessageHandler(Filters.regex(re.compile(r"bus(?:es)?", re.IGNORECASE)), main_menu_handler)
])
