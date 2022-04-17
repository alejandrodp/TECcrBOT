from tcrb.apps import main_menu
from tcrb.apps.directory.settings import DIRECTORY_HANDLERS
from tcrb.apps.search.settings import SEARCH_HANDLERS
from tcrb.apps.tracking.settings import TRACKING_HANDLERS
from tcrb.apps.transportation.settings import TRANSPORTATION_HANDLERS
from tcrb.pages import PAGE_HANDLER_CONFIGS


class Handlers:
    def __init__(self, handler_configs):

        self._handlers = {}
        self._create_handlers(handler_configs)

    @property
    def handlers(self):
        return self._handlers

    def _create_handlers(self, handler_configs):
        from tcrb.core.handlers import HandlerConfig
        if not all(isinstance(app, HandlerConfig) for app in handler_configs):
            raise f"All configurations must be instances of {HandlerConfig.__name__}"

        for app in handler_configs:
            self._handlers.setdefault(app.group, []).extend(app.handlers)


apps = Handlers([
    main_menu.MAIN_MENU_HANDLERS,
    main_menu.COMMAND_HANDLERS,
    PAGE_HANDLER_CONFIGS,
    TRACKING_HANDLERS,
    TRANSPORTATION_HANDLERS,
    DIRECTORY_HANDLERS,
    # Mantener handlers de búsqueda de último, son los que reciben el texto no reconocido anteriormente.
    SEARCH_HANDLERS,
])
