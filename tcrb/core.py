import importlib
from enum import Enum

from django.conf import settings
from django.core.paginator import Paginator
from telegram import InlineKeyboardButton
from telegram.ext import MessageHandler, Filters, CallbackQueryHandler

from common.util import InlinePaginatorCustom


class BotAppConfig:
    handlers = []
    main_menu = []

    def __init__(self, config):
        self.ty = config.name
        self.title = config.verbose_name

    def add_main_menu_entry(self, handler):
        if not BotAppConfig.main_menu or len(BotAppConfig.main_menu[-1]) >= 2:
            BotAppConfig.main_menu.append([])

        BotAppConfig.main_menu[-1].append(self.title)
        BotAppConfig.add_message_handler(Filters.text(self.title), handler)

    def create_inline_button(self, sub_type, *patterns):
        return BotAppConfig.InlineButton(sub_type, self, *patterns)

    def create_paginator(self, sub_type, *patterns):
        return BotAppConfig.InlineButton(sub_type, self, rf"(\d+)", *patterns)

    @staticmethod
    def get_handlers():
        _ = {app: importlib.import_module('.settings', app) for app in settings.BOT_APPS}
        return BotAppConfig.handlers

    @staticmethod
    def add_message_handler(filters, callback):
        BotAppConfig.handlers.append(MessageHandler(filters, callback))

    @staticmethod
    def _parse_sub_type(sub_type):
        if isinstance(sub_type, Enum):
            return sub_type.value
        return sub_type

    class InlineButton:
        pattern_separator = ":"

        def __init__(self, sub_type, config, *patterns):
            self.sub_type = sub_type
            self.config = config
            self.patterns = patterns

        def build_button(self, text, *data, **kwargs):
            return InlineKeyboardButton(
                text=text,
                callback_data=self._build_handler_callback_data(self.sub_type, False, *data),
                **kwargs)

        def _build_handler_callback_data(self, sub_type, isHandler: bool, *data):
            sub_type = BotAppConfig._parse_sub_type(sub_type)

            data = self.pattern_separator.join(str(j)
                                               for i in (self.config.ty, sub_type, data)
                                               for j in (i if isinstance(i, tuple) else (i,)))
            if isHandler:
                data = f'^{data}$'

            print(data)
            return data

        def init_handler(self, callback):
            BotAppConfig.handlers.append(
                CallbackQueryHandler(callback,
                                     pattern=self._build_handler_callback_data(
                                         self.sub_type,
                                         True,
                                         *self.patterns
                                     ))
            )

        def build_paginator(self, current_page, pages: Paginator, buttons, *data):
            paginator = InlinePaginatorCustom(
                page_count=pages.num_pages,
                current_page=current_page,
                data_pattern=self._build_handler_callback_data(self.sub_type, False, '{page}', *data)
            )

            paginator.add_before(*buttons)

            return paginator

