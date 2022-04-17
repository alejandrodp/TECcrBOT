import base
import telegram.ext


class CommandHandler(base.BaseHandler):
    def __init__(self, text, callback):
        super().__init__(callback,
                         lambda cb: telegram.ext.CommandHandler(text, cb))
