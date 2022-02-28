from telegram import Update
from telegram.error import BadRequest

from tcrb.apps import main_menu


class Reply:
    def __init__(self, update: Update):
        self._update = update
        self._has_failed = False
        self._buffered = ''

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
        message = self._message()
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

    def buffer_text(self, text):
        self._buffered += text

    def text(self, text, **kwargs):
        # No utlizar con actualizaciones del tipo InlineQuery
        update = self._read_update()
        if self._buffered:
            text = (self._buffered + text).strip()
            self._buffered = ''
        message = self._message()

        if update.callback_query and update.callback_query.message:
            try:
                return message.edit_text(text, **kwargs)
            except BadRequest:
                return message
        else:
            return message.reply_text(text, **kwargs) \
                if kwargs.get("reply_markup") \
                else message.reply_text(text, reply_markup=main_menu.MAIN_MENU_HANDLERS.keyboard_markup(), **kwargs)

    def edit_markup(self, reply_markup):
        message = self._message()
        try:
            return message.edit_reply_markup(reply_markup)
        except BadRequest:
            return message

    def _message(self):
        update = self._read_update()
        if update.message:
            message = update.message
        elif update.edited_message:
            message = update.edited_message
        elif update.channel_post:
            message = update.channel_post
        elif update.edited_channel_post:
            message = update.edited_channel_post
        elif update.callback_query and update.callback_query.message:
            message = update.callback_query.message
        else:
            raise AttributeError("There is no message in this update")

        return message

    def bad_request(self):
        self.fail('Error de formato de solicitud, favor reporte este incidente.')

    def expect(self, condition):
        if not condition:
            self.bad_request()

    def user_first_name(self):
        return self._effective_user().first_name

    def user_id(self):
        return self._effective_user().id

    def _effective_user(self):
        effective_user = self._read_update().effective_user
        assert effective_user, "This update has no user"
        return effective_user

    def expect_int(self, maybe_int):
        try:
            return int(maybe_int)
        except ValueError:
            self.expect(False)

    def _read_update(self):
        assert self._update is not None
        return self._update


class ReplyExit(Exception):
    pass
