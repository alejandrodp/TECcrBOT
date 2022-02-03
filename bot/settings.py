from django.conf import settings
import importlib

from telegram.ext import Filters

from bot.handlers import handlers, type_handler, show_page, main_menu, search_handler
from bot.menu import add_command_handler, add_message_handler

handlers.add_callback_query_handler(type_handler, 'get_type_pages', r'(\d+)')
handlers.add_callback_query_handler(show_page, 'get_page', r'(\d+)', r'(\d+)')
add_command_handler("menu", main_menu)
add_command_handler("start", main_menu)

APP_CONFIGS = {app: importlib.import_module(
    '.settings', app) for app in settings.BOT_APPS}

add_message_handler(Filters.text & ~Filters.command,
                    search_handler)
