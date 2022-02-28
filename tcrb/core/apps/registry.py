from tcrb.core.apps.handlers.config import HandlerConfig


class Apps:
    def __init__(self, handler_configs):

        self._handlers = {}
        self._create_handlers(handler_configs)

    @property
    def handlers(self):
        return self._handlers

    def _create_handlers(self, handler_configs):
        if not all(isinstance(app, HandlerConfig) for app in handler_configs):
            raise f"All configurations must be instances of {HandlerConfig.__name__}"

        for app in handler_configs:
            self._handlers.setdefault(app.group, []).extend(app.handlers)


class Pages:
    def __init__(self, page_configs):
        self._page_tys = {}
        self._create_pages(page_configs)

    @property
    def page_tys(self):
        return self._page_tys

    def _create_pages(self, page_configs):
        for page in page_configs:
            existing = self._page_tys.get(page.ty)
            if existing:
                raise ValueError(f"Page type `{page.desc}` collides with `{existing.desc}`")
            self._page_tys[page.ty] = page
