from telegram.ext import CallbackQueryHandler

from bot.menu import main_menu_entry
from tcrb.core import PageTy
from . import apps
from .models import Service
from .handlers import main_entry, process_service
from .util import index_services

HANDLERS = [
    main_menu_entry('Servicios generales \U0001f3eb', main_entry),
    CallbackQueryHandler(
        process_service, pattern=rf'{apps.ServicesConfig.name}:selecting_service:\d*')
]

PageTy(ty=0, model=Service, desc='Servicios', index=index_services, build=None)
