from tcrb.apps import main_menu
from tcrb.apps.pages.settings import PAGE_HANDLER_CONFIGS
from tcrb.apps.places.settings import PLACES_PAGE
from tcrb.apps.search.settings import SEARCH_HANDLERS
from tcrb.apps.services.settings import SERVICES_PAGE
from tcrb.apps.config import Handlers
from tcrb.apps.config import Pages

pages = Pages([
    SERVICES_PAGE,
    PLACES_PAGE
])

apps = Handlers([
    main_menu.MAIN_MENU_HANDLERS,
    main_menu.COMMAND_HANDLERS,
    PAGE_HANDLER_CONFIGS,
    SEARCH_HANDLERS,
])
