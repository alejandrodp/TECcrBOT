from telegram.ext import MessageHandler, Filters, CallbackQueryHandler

from common.util import RegexReplyMessageFilter
from . import apps
from .handlers import menu_entry, select_place, get_place, handle_text_edit, select_edit, request_edit

MAIN_MENU_COMMAND = 'Ubicaciones 📍'

HANDLERS = [
    MessageHandler(Filters.text(MAIN_MENU_COMMAND), menu_entry),
    CallbackQueryHandler(select_place, pattern=rf'{apps.PlacesConfig.name}:tag_id:\d*'),
    CallbackQueryHandler(get_place, pattern=rf'{apps.PlacesConfig.name}:place_id:.*'),
    CallbackQueryHandler(select_edit, pattern=rf'{apps.PlacesConfig.name}:select_edit:\d+'),
    CallbackQueryHandler(request_edit, pattern=rf'{apps.PlacesConfig.name}:request_edit:\d+:\d+'),
    MessageHandler(Filters.reply &
                   (Filters.text | Filters.photo | Filters.location) &
                   RegexReplyMessageFilter(r'(?:^Sugerencia de .* para el lugar .*\n.*\nDatos: )(.*)'),
                   handle_text_edit)
]
