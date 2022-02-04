import importlib

from django.conf import settings
from telegram import InlineKeyboardButton
from telegram.ext import MessageHandler, Filters


class BotAppConfig:
    handlers = []
    pattern_separator = ":"
    main_menu = []

    class InlineButton:
        def __init__(self, sub_type, master):
            self.sub_type = sub_type
            self.master = master

        def __call__(self, text, *data, **kwargs):
            return InlineKeyboardButton(
                text=text,
                callback_data=self.master._build_handler_callback_data(self.sub_type, False, *data),
                **kwargs)

    def __init__(self, config):
        self.ty = config.name
        self.title = config.verbose_name

    def main_menu_entry(self, handler):
        if not BotAppConfig.main_menu or len(BotAppConfig.main_menu[-1]) >= 2:
            BotAppConfig.main_menu.append([])

        BotAppConfig.main_menu[-1].append(self.title)
        BotAppConfig.add_message_handler(Filters.text(self.title), handler)

    @staticmethod
    def get_handlers():
        _ = {app: importlib.import_module('.settings', app) for app in settings.BOT_APPS}
        return BotAppConfig.handlers

    @staticmethod
    def add_message_handler(filters, callback):
        BotAppConfig.handlers.append(MessageHandler(filters, callback))
