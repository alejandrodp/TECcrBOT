from tcrb.core import PageTy
from .apps import PlacesConfig
from .buttons import config, list_categories, list_categories_paginator, list_places, list_places_paginator
from .constants import PAGE_TY
from .handlers import menu_entry, first_category_list, remain_category_list, first_place_list, remain_place_list
from .util import index_places, show_place

config.add_main_menu_entry(menu_entry)
list_categories.init_handler(first_category_list)
list_categories_paginator.init_handler(remain_category_list)
list_places.init_handler(first_place_list)
list_places_paginator.init_handler(remain_place_list)


PLACE_PAGES = PageTy(PAGE_TY, PlacesConfig.verbose_name, index_places, show_place)
