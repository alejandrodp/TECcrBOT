from enum import Enum
from typing import Union

from django.core.paginator import Paginator
from telegram import InlineKeyboardButton
from telegram.ext import MessageHandler, Filters, CallbackQueryHandler, CommandHandler

from common.util import InlinePaginatorCustom

_main_menu = []


def read_main_menu():
    return _main_menu


def main_menu_entry(title, handler):
    if not _main_menu or len(_main_menu[-1]) >= 2:
        _main_menu.append([])

    _main_menu[-1].append(title)
    add_message_handler(Filters.text(title), handler)


def add_message_handler(filters, callback):
    BotHandler._handlers.append(MessageHandler(filters, callback))


def add_command_handler(command, callback):
    BotHandler._handlers.append(CommandHandler(command, callback))


def build_page_button(text, ty, page_id):
    from bot.handlers import handlers
    return handlers.build_inline_button(text, 'get_page', ty, page_id)


def _parse_sub_type(sub_type):
    if isinstance(sub_type, Enum):
        return sub_type.value
    return sub_type


class BotHandler:
    _handlers = []

    def __init__(self, ty: str):
        self.ty = ty
        self.pattern_separator = ':'

    def _build_handler_callback_data(self, sub_type, ishandler: bool, *data):
        sub_type = _parse_sub_type(sub_type)

        data = self.pattern_separator.join(j
                                           for i in (self.ty, sub_type, data)
                                           for j in (i if isinstance(i, tuple) else (i,)))

        if ishandler:
            data = f'^{data}$'

        return data

    def add_callback_query_handler(self, callback, sub_type, *patterns):
        BotHandler._handlers.append(CallbackQueryHandler(callback,
                                                         pattern=self._build_handler_callback_data(
                                                             sub_type, True, *patterns)))

    def build_inline_button(self, text: str, sub_type: Union[Enum, str], *data, **kwargs):
        return InlineKeyboardButton(
            text=text,
            callback_data=self._build_handler_callback_data(sub_type, False, *data),
            **kwargs)

    def build_paginator(self, current_page, sub_type, pages: Paginator, buttons: list):
        paginator = InlinePaginatorCustom(
            page_count=pages.num_pages,
            current_page=current_page,
            data_pattern=self._build_handler_callback_data(sub_type, False, '{page}')
        )

        paginator.add_before(*buttons)

        return paginator

    def add_paginator_handler(self, callback, sub_type):
        self.add_callback_query_handler(callback, sub_type, r"(\d+)")
