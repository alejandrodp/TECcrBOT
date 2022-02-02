from telegram.ext import MessageHandler, Filters, CallbackQueryHandler

from bot.pages import PageTy
from . import apps
from .handlers import main_entry, process_service
from .util import index_services

MAIN_MENU_COMMAND = 'Servicios generales 🏫'

HANDLERS = [
    MessageHandler(Filters.text(MAIN_MENU_COMMAND), main_entry),
    CallbackQueryHandler(process_service, pattern=rf'{apps.ServicesConfig.name}:selecting_service:\d*')
]

PageTy(0, 'Servicios', index_services)
