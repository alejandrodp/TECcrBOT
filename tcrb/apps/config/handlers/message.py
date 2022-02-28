from .base import BaseHandler
from telegram.ext import MessageHandler as _MessageHandler


class MessageHandler(BaseHandler):
    def __init__(self, filters, callback):
        super().__init__(callback, lambda cb: _MessageHandler(filters, cb))
