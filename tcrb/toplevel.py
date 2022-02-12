import importlib

from telegram.ext import Filters

from .settings import BOT_APPS
from .buttons import page_button, config, one_type_paginator, type_selection_button, multiple_types_paginator
from .handlers import main_menu, show_page_handler, search_handler, send_one_type_page_handler, \
    type_selection_handler, \
    send_multiple_type_pages_handler, greetings_message_handler, info_message_handler

config.add_main_menu_entry(info_message_handler)
config.add_command_handler("menu", main_menu)
config.add_command_handler("start", greetings_message_handler)
config.add_command_handler("help", greetings_message_handler)
page_button.init_handler(show_page_handler)
config.add_message_handler(Filters.text & ~Filters.command & ~Filters.update.edited_message, search_handler)

one_type_paginator.init_handler(send_one_type_page_handler)

multiple_types_paginator.init_handler(send_multiple_type_pages_handler)

type_selection_button.init_handler(type_selection_handler)

for _app in BOT_APPS:
    importlib.import_module('.settings', _app)
