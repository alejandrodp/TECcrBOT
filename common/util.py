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
            suppress = isinstance(exc_value, ReplyExit)
            if not suppress:
                self.fail("Ocurrió un problema, intente nuevamente.", exit_now=False)

            return suppress

    def text_query(self):
        message = self._read_update().message
        assert message, "This update has no message.text"
        return message.text

    def callback_query(self):
        cq = self._read_update().callback_query
        assert cq, "This update lacks a callback_query"
        return cq

    def fail(self, error, *, exit_now=True):
        if not self._has_failed:
            self._has_failed = True

            self._update.effective_chat.send_message(error)
            self._update = None

        if exit_now:
            raise ReplyExit()

    def text(self, text, **kwargs) -> Message:
        update = self._read_update()
        if update.message:
            return update.message.reply_text(text, **kwargs)
        else:
            return update.callback_query.edit_message_text(text, **kwargs)

    def bad_request(self):
        self.fail('Error de formato de solicitud, favor reporte este incidente.')

    def expect(self, condition):
        if not condition:
            self.bad_request()

    def expect_int(self, maybe_int):
        try:
            return int(maybe_int)
        except ValueError:
            self.expect(False)

    def expect_idx(self, lst, index):
        self.expect(0 <= index < len(lst))
        return lst[index]

    def _read_update(self):
        assert self._update is not None
        return self._update


class ReplyExit(Exception):
    pass
