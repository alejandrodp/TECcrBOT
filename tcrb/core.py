from enum import Enum

from django.conf import settings
from django.core.paginator import Paginator
from telegram import Update, InlineKeyboardButton
from telegram.ext import CallbackContext, MessageHandler, Filters, CallbackQueryHandler, CommandHandler

from .common.util import InlinePaginatorCustom, Reply


class BotAppConfig:
    _handlers = []
    _main_menu = []

    def __init__(self, name, title):
        self.ty = name
        self.title = title

    def add_main_menu_entry(self, handler):
        if not BotAppConfig._main_menu or len(BotAppConfig._main_menu[-1]) >= 2:
            BotAppConfig._main_menu.append([])

        BotAppConfig._main_menu[-1].append(self.title)
        BotAppConfig.add_message_handler(Filters.text(self.title), handler)

    def create_inline_button(self, sub_type, *patterns):
        return BotAppConfig.InlineButton(sub_type, self, *patterns)

    def create_paginator(self, sub_type, *patterns):
        return BotAppConfig.InlineButton(sub_type, self, "pages", rf"(\d+)", *patterns)

    @staticmethod
    def get_main_menu():
        BotAppConfig.load_settings()
        return BotAppConfig._main_menu

    @staticmethod
    def load_settings():
        from . import toplevel as _

    @staticmethod
    def get_handlers():
        BotAppConfig.load_settings()
        return BotAppConfig._handlers

    @staticmethod
    def add_command_handler(text, callback):
        BotAppConfig._add_handler(
            callback, lambda cb: CommandHandler(text, cb))

    @staticmethod
    def add_message_handler(filters, callback):
        BotAppConfig._add_handler(
            callback, lambda cb: MessageHandler(filters, cb))

    @staticmethod
    def _parse_sub_type(sub_type):
        if isinstance(sub_type, Enum):
            return sub_type.value
        return sub_type

    @staticmethod
    def _add_handler(callback, make_handler):
        def wrapped(update: Update, context: CallbackContext):
            with Reply(update) as reply:
                callback(reply, context)

        BotAppConfig._handlers.append(make_handler(wrapped))

    class InlineButton:
        pattern_separator = ":"

        def __init__(self, sub_type, config, *patterns):
            self.sub_type = sub_type
            self.config = config
            self.patterns = patterns

        def build_button(self, text, *data, **kwargs):
            return InlineKeyboardButton(
                text=text,
                callback_data=self._build_callback_data(
                    self.sub_type, False, *data),
                **kwargs)

        def _build_callback_data(self, sub_type, isHandler: bool, *data):
            sub_type = BotAppConfig._parse_sub_type(sub_type)

            data = self.pattern_separator.join(str(j)
                                               for i in (self.config.ty, str(sub_type), data)
                                               for j in (i if isinstance(i, tuple) else (i,)))
            if isHandler:
                data = f'^{data}$'

            return data

        def init_handler(self, callback):
            pattern = self._build_callback_data(
                self.sub_type, True, *self.patterns)
            BotAppConfig._add_handler(
                callback, lambda cb: CallbackQueryHandler(cb, pattern=pattern))

        def build_paginator(self, current_page_index, objects, buttons_factory, *data):

            pages = Paginator(objects, settings.
                              PAGINATION_LIMIT)

            current_page = pages.get_page(current_page_index)

            buttons = buttons_factory(current_page)

            paginator = InlinePaginatorCustom(
                page_count=pages.num_pages,
                current_page=current_page_index,
                data_pattern=self._build_callback_data(
                    self.sub_type, False, "pages", '{page}', *data)
            )

            paginator.add_before(*buttons)

            return paginator


class PageTy:
    _tys = {}

    def __init__(self, *, ty, model, desc, build, index=None):
        existing = PageTy._tys.get(ty)
        assert existing is None, f'Page type `{desc}` collides with `{existing.desc}`'

        self.ty = ty
        self.desc = desc
        self.model = model
        self.index = index
        self.builder = build
        PageTy._tys[ty] = self

    @staticmethod
    def read_page_tys():
        BotAppConfig.load_settings()
        return PageTy._tys
