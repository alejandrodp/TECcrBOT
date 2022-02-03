from telegram import InlineKeyboardButton
from telegram.ext import MessageHandler, Filters, CallbackQueryHandler

_main_menu = []


def read_main_menu():
    import bot.settings as _
    return _main_menu


def main_menu_entry(title, handler):
    if not _main_menu or len(_main_menu[-1]) >= 2:
        _main_menu.append([])

    _main_menu[-1].append(title)
    # return MessageHandler(Filters.text(title), handler)
    add_message_handler(Filters.text(title), handler)


def add_message_handler(filters, callback):
    BotHandler._handlers.append(MessageHandler(filters, callback))


class BotHandler:
    _handlers = []

    def __init__(self, ty: str):
        self.ty = ty
        self.pattern_separator = ':'

    def _build_handler_callback_data(self, sub_type, data):
        return self.pattern_separator.join(x for mierda in (data, (self.ty, sub_type)) for x in mierda)

    def add_callback_query_handler(self, callback, sub_type, *pattern):
        BotHandler._handlers.append(CallbackQueryHandler(callback,
                                                         pattern=self._build_handler_callback_data(
                                                            sub_type, pattern)))

    def build_inline_button(self, text, sub_type, *data):
        return InlineKeyboardButton(
            text=text,
            callback_data=self._build_handler_callback_data(sub_type, data))
