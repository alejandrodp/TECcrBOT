import string

from telegram import Chat, Update, Message
from telegram.ext import Filters
from telegram_bot_pagination import InlineKeyboardPaginator


class RegexReplyMessageFilter(Filters.regex):
    def filter(self, message):
        return super().filter(message.reply_to_message)


class InlinePaginatorCustom(InlineKeyboardPaginator):
    def add_before(self, *inline_buttons):
        for button in inline_buttons:
            self._keyboard_before.append([{
                'text': button.text,
                'callback_data': button.callback_data,
            }])


class Reply:
    def __init__(self, update: Update):
        self._update = update
        self._has_failed = False

    def __enter__(self):
        if self._update.callback_query:
            self._update.callback_query.answer()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value is not None:
            self.unknown_error()

    def text_query(self):
        message = self._read_update().message
        assert message, "This update has no message.text"
        return message.text

    def callback_query(self):
        cq = self._read_update().callback_query
        assert cq, "This update lacks a callback_query"
        return cq

    def unknown_error(self):
        if not self._has_failed:
            self._has_failed = True

            MSG = "Ocurrió un problema, intente nuevamente."
            self._update.effective_chat.send_message(MSG)
            self._update = None

    def text(self, text, **kwargs) -> Message:
        update = self._read_update()
        if update.message:
            return update.message.reply_text(text, **kwargs)
        else:
            return update.callback_query.edit_message_text(text, **kwargs)

    def _read_update(self):
        assert self._update is not None
        return self._update


def is_int(*text: str):
    return all(s in string.digits for elm in text for s in elm)
