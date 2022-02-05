from telegram.ext import Filters
from bot.buttons import page_button, config, one_type_paginator, type_selection_button, multiple_types_paginator
from bot.handlers import main_menu, show_page_handler, search_handler, send_one_type_page, type_selection, \
    send_multiple_type_pages

config.add_command_handler("menu", main_menu)
page_button.init_handler(show_page_handler)
config.add_message_handler(Filters.text & ~Filters.command, search_handler)

one_type_paginator.init_handler(send_one_type_page)

multiple_types_paginator.init_handler(send_multiple_type_pages)

type_selection_button.init_handler(type_selection)