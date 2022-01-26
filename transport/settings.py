from telegram.ext import MessageHandler, CallbackQueryHandler, Filters

from transport import apps
from transport.handlers import menu_entry, process_type, process_travel

MAIN_MENU_COMMAND = 'Servicios de transporte 🚌'

HANDLERS = [

    MessageHandler(Filters.text(MAIN_MENU_COMMAND), menu_entry),
    CallbackQueryHandler(process_type, pattern=rf"{apps.TransportConfig.name}:t_type:\d*"),
    CallbackQueryHandler(process_travel, pattern=rf"{apps.TransportConfig.name}:travel:\d*")

]