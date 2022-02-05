from telegram.ext import CallbackQueryHandler

from bot.menu import main_menu_entry
from transportation import apps
from transportation.handlers import menu_entry, get_routes, get_schedule

from tcrb.core import PageTy
from transportation.util import index_route, route_builder

HANDLERS = [
    main_menu_entry('Servicios de transporte \U0001f68c', menu_entry),
    CallbackQueryHandler(
        get_routes, pattern=rf"{apps.TransportationConfig.name}:vehicle:\d+"),
    CallbackQueryHandler(
        get_schedule, pattern=rf"{apps.TransportationConfig.name}:route:\d+"),
]

ROUTE_PAGES = PageTy(5, 'Rutas', index_route, route_builder)