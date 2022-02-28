from .constants import PEOPLE_TY, DEPT_TY, LOC_TY
from .models import Person, Unit, Location
from .util import index_people, people_builder, depts_page_builder, loc_builder
from ...core.apps.pages import PageTy

PEOPLE_PAGES = PageTy(ty=PEOPLE_TY, model=Person,
                      desc='personas', index=index_people, build=people_builder)

DEPT_PAGES = PageTy(ty=DEPT_TY, model=Unit, desc='departamentos', build=depts_page_builder)

LOC_PAGES = PageTy(ty=LOC_TY, model=Location, desc='campuses', build=loc_builder)
