class BaseHandler:
    def __init__(self, callback, make_handler):
        def wrapped(update, context):
            from .reply import Reply
            with Reply(update) as reply:
                callback(reply, context)

        self._wrapped = wrapped
        self._make_handler = make_handler

    def make_handler(self):
        if not hasattr(self, "_make_handler"):
            raise AttributeError("_make_handler attribute is not set, initialize the base handler first")
        return self._make_handler(self._wrapped)
