from tcrb.apps import main_menu
from tcrb.apps.config.registry import Pages, Handlers
from tcrb.apps.directory.settings import PEOPLE_PAGES, DEPT_PAGES, LOC_PAGES, DIRECTORY_HANDLERS
from tcrb.apps.pages.settings import PAGE_HANDLER_CONFIGS
from tcrb.apps.places.settings import PLACES_PAGE
from tcrb.apps.search.settings import SEARCH_HANDLERS
from tcrb.apps.services.settings import SERVICES_PAGE
from tcrb.apps.tracking.settings import TRACKING_HANDLERS
from tcrb.apps.transportation.settings import TRANSPORTATION_HANDLERS

all_pages = Pages([
    SERVICES_PAGE,
    PLACES_PAGE,
    PEOPLE_PAGES,
    DEPT_PAGES,
    LOC_PAGES,
])

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
