from .base import BaseHandler
from telegram.ext import CallbackQueryHandler as _CallbackQueryHandler


class CallbackQueryHandler(BaseHandler):
    def __init__(self, button, callback):
        self.button = button
        super().__init__(callback,
                         lambda cb: _CallbackQueryHandler(cb, pattern=self.button.match_pattern))
