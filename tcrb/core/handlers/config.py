import telegram.ext


class HandlerConfig:
    def __init__(self, handlers, group=telegram.ext.dispatcher.DEFAULT_GROUP):
        from .base import BaseHandler
        if not all(isinstance(handler, BaseHandler) for handler in handlers):
            raise ValueError(f"All handlers should be a subclass of {BaseHandler.__name__}")

        self._handlers = []
        self._group = group

        for handler in handlers:
            self._handlers.append(handler.make_handler())

    @property
    def group(self):
        return self._group

    @property
    def handlers(self):
        return self._handlers
