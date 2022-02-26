from tcrb.app.config import PageTy
from .buttons import config
from .constants import PAGE_TY
from .handlers import menu_entry
from .models import Place
from .util import show_place

config.add_main_menu_entry(menu_entry)


PLACE_PAGES = PageTy(ty=PAGE_TY, model=Place, desc='ubicaciones', build=show_place)
