from tcrb.apps import main_menu
from tcrb.apps.pages.settings import PAGE_HANDLER_CONFIGS
from tcrb.apps.search.settings import SEARCH_HANDLERS
from tcrb.apps.services.settings import SERVICES_PAGE
from tcrb.core.apps import Apps
from tcrb.core.apps.registry import Pages

pages = Pages([
    SERVICES_PAGE,
])

apps = Apps([
    main_menu.MAIN_MENU_HANDLERS,
    main_menu.COMMAND_HANDLERS,
    PAGE_HANDLER_CONFIGS,
    SEARCH_HANDLERS,
])
