from .handlers import *
from .util import index_places, show_place

config.add_main_menu_entry(menu_entry)
list_categories.init_handler(first_category_list)
list_categories_paginator.init_handler(remain_category_list)
list_places.init_handler(first_place_list)
list_places_paginator.init_handler(remain_place_list)


PLACES_PAGES = config.set_page_settings(PAGE_TY, index_places, show_place)
