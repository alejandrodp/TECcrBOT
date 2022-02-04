from bot.menu import main_menu_entry
from bot.pages import PageTy
from .apps import PlacesConfig
from .constants import PAGE_TY

from .handlers import menu_entry, first_category_list, States, remain_category_list, handlers, \
    first_place_list, remain_place_list
from .util import index_places, show_place

main_menu_entry(PlacesConfig.verbose_name, menu_entry)
handlers.add_callback_query_handler(first_category_list, States.SELECT_CATEGORY)
handlers.add_paginator_handler(remain_category_list, States.SELECT_CATEGORY)
handlers.add_callback_query_handler(first_place_list, States.GET_PLACES, r'(\d+)')
handlers.add_paginator_handler(remain_place_list, States.GET_PLACE, r'(\d+)')


PLACE_PAGES = PageTy(PAGE_TY, PlacesConfig.verbose_name, index_places, show_place)
