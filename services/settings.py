from telegram.ext import CallbackQueryHandler

from bot.menu import main_menu_entry
from bot.pages import PageTy
from . import apps
from .handlers import main_entry, process_service
from .util import index_services

HANDLERS = [
    main_menu_entry('Servicios generales \U0001f3eb', main_entry),
    CallbackQueryHandler(process_service, pattern=rf'{apps.ServicesConfig.name}:selecting_service:\d*')
]

PageTy(0, 'Servicios', index_services, None)
