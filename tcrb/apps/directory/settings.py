from .models import Person, Unit, Location
from .util import index_people, people_builder, dept_builder, loc_builder
from tcrb.apps.config.pages import PageTy

PEOPLE_PAGES = PageTy(ty=1, model=Person,
                      desc='personas', index=index_people, build=people_builder)

DEPT_PAGES = PageTy(ty=2, model=Unit, desc='departamentos', build=dept_builder)

LOC_PAGES = PageTy(ty=3, model=Location, desc='campuses', build=loc_builder)
