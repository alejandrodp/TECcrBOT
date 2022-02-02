from telegram.ext import MessageHandler, Filters, CallbackQueryHandler

from . import apps
from .handlers import main_entry, process_service
from .util import index

MAIN_MENU_COMMAND = 'Servicios generales 🏫'

HANDLERS = [
    MessageHandler(Filters.text(MAIN_MENU_COMMAND), main_entry),
    CallbackQueryHandler(process_service, pattern=rf'{apps.ServicesConfig.name}:selecting_service:\d*')
]

PAGE_TY = 0
PAGE_INDEX = index
PAGE_DESC = 'Servicios'
