from .models import Place
from .util import show_place
from ...core.apps.pages import PageTy

PLACES_DESC = "Ubicaciones \U0001f4cd"

PLACES_PAGE = PageTy(ty=4, model=Place, desc=PLACES_DESC, build=show_place)
