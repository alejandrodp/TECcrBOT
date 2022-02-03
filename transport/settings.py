from telegram.ext import CallbackQueryHandler

from bot.menu import main_menu_entry
from transport import apps
from transport.handlers import menu_entry, process_type, process_travel

HANDLERS = [
    main_menu_entry('Servicios de transporte \U0001f68c', menu_entry),
    CallbackQueryHandler(process_type, pattern=rf"{apps.TransportConfig.name}:t_type:\d*"),
    CallbackQueryHandler(process_travel, pattern=rf"{apps.TransportConfig.name}:travel:\d*")
]
