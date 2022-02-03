from telegram.ext import Filters

from bot.menu import main_menu_entry, BotHandler, add_message_handler
from bot.pages import PageTy
from common.util import RegexReplyMessageFilter
from . import apps
from .handlers import menu_entry, select_place, get_place, handle_text_edit, select_edit, request_edit, handlers
from .util import index_places, show_place

main_menu_entry('Ubicaciones \U0001f4cd', menu_entry)
handlers.add_callback_query_handler(select_place, 'tag_id', r'\d+')
handlers.add_callback_query_handler(get_place, 'place_id', r'\d+')
handlers.add_callback_query_handler(select_edit, 'select_edit', r'\d+')
handlers.add_callback_query_handler(request_edit, 'request_edit', r'\d+', r'\d+')
add_message_handler(Filters.reply &
                    (Filters.text | Filters.photo | Filters.location) &
                    RegexReplyMessageFilter(
                        r'(?:^Sugerencia de .* para el lugar .*\n.*\nDatos: )(.*)'),
                    handle_text_edit)

PLACE_PAGES = PageTy(4, 'Lugares', index_places, show_place)

# HANDLERS = [
#     ,
#     CallbackQueryHandler(
#         select_place, pattern=rf'{apps.PlacesConfig.name}:tag_id:\d*'),
#     CallbackQueryHandler(
#         get_place, pattern=rf'{apps.PlacesConfig.name}:place_id:.*'),
#     CallbackQueryHandler(
#         select_edit, pattern=rf'{apps.PlacesConfig.name}:select_edit:\d+'),
#     CallbackQueryHandler(
#         request_edit, pattern=rf'{apps.PlacesConfig.name}:request_edit:\d+:\d+'),
#     MessageHandler(Filters.reply &
#                    (Filters.text | Filters.photo | Filters.location) &
#                    RegexReplyMessageFilter(
#                        r'(?:^Sugerencia de .* para el lugar .*\n.*\nDatos: )(.*)'),
#                    handle_text_edit)
# ]
