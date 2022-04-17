from . import base
import telegram.ext


class MessageHandler(base.BaseHandler):
    def __init__(self, filters, callback):
        super().__init__(callback, lambda cb: telegram.ext.MessageHandler(filters, cb))
