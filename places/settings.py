from bot.menu import main_menu_entry
from bot.pages import PageTy
from .apps import PlacesConfig

from .handlers import menu_entry, select_place, get_place, handlers, select_category, States
from .util import index_places, show_place

main_menu_entry(PlacesConfig.verbose_name, menu_entry)
handlers.add_callback_query_handler(select_place, 'tag_id', r'\d+')
handlers.add_callback_query_handler(get_place, 'place_id', r'\d+')
handlers.add_callback_query_handler(select_category, States.SELECT_CATEGORY)
handlers.add_callback_query_handler(select_category, States.SELECT_CATEGORY, r'(\d+)')


PLACE_PAGES = PageTy(4, PlacesConfig.verbose_name, index_places, show_place)
