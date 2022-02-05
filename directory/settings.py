from tcrb.core import PageTy
from .buttons import see_department, department_people_paginator
from .constants import PEOPLE_TY, DEPT_TY, LOC_TY
from .handlers import show_department, depts_people_pagination
from .util import index_people, index_depts, index_locs, people_builder, depts_page_builder, loc_builder

PEOPLE_PAGES = PageTy(PEOPLE_TY, 'Personas', index_people, people_builder)
DEPT_PAGES = PageTy(DEPT_TY, 'Departamentos', index_depts, depts_page_builder)
LOC_PAGES = PageTy(LOC_TY, 'Campuses', index_locs, loc_builder)

see_department.init_handler(show_department)

department_people_paginator.init_handler(depts_people_pagination)
