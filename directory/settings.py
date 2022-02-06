from tcrb.core import PageTy
from .buttons import see_department, department_people_paginator
from .constants import PEOPLE_TY, DEPT_TY, LOC_TY
from .handlers import show_department, depts_people_pagination
from .models import Person, Unit, Location
from .util import index_people, people_builder, depts_page_builder, loc_builder

PEOPLE_PAGES = PageTy(ty=PEOPLE_TY, model=Person,
                      desc='Personas', index=index_people, build=people_builder)

DEPT_PAGES = PageTy(ty=DEPT_TY, model=Unit, desc='Departamentos', build=depts_page_builder)

LOC_PAGES = PageTy(ty=LOC_TY, model=Location, desc='Campuses', build=loc_builder)

see_department.init_handler(show_department)

department_people_paginator.init_handler(depts_people_pagination)
