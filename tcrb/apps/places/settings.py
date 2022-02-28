from .constants import PAGE_TY
from .models import Place
from .util import show_place
from ...core.apps.pages import PageTy

PLACE_PAGES = PageTy(ty=PAGE_TY, model=Place, desc='Ubicaciones', build=show_place)
