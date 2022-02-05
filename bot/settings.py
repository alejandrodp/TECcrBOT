from bot.buttons import page_button, config
from bot.handlers import main_menu, show_page_handler

config.add_command_handler("menu", main_menu)
page_button.init_handler(show_page_handler)

# add_command_handler("menu", main_menu)
# add_command_handler("start", main_menu)
# handlers.add_callback_query_handler(type_handler, 'get_type_pages', r'(\d+)')
# handlers.add_callback_query_handler(show_page, 'get_page', r'(\d+)', r'(\d+)')
#
#
#
# add_message_handler(Filters.text & ~Filters.command,
#                     search_handler)
