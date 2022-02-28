from .base import BaseHandler
from telegram.ext import CommandHandler as _CommandHandler


class CommandHandler(BaseHandler):
    def __init__(self, text, callback):
        super().__init__(callback,
                         lambda cb: _CommandHandler(text, cb))
