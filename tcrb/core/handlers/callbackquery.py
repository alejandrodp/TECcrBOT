import base
import telegram.ext


class CallbackQueryHandler(base.BaseHandler):
    def __init__(self, button, callback):
        self.button = button
        super().__init__(callback,
                         lambda cb: telegram.ext.CallbackQueryHandler(cb, pattern=self.button.match_pattern))
