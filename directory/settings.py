from tcrb.core import PageTy
from .buttons import see_department
from .handlers import show_department
from .util import index_people, index_depts, index_locs, people_builder, depts_builder, loc_builder

PEOPLE_PAGES = PageTy(1, 'Personas', index_people, people_builder)
DEPT_PAGES = PageTy(2, 'Departamentos', index_depts, depts_builder)
LOC_PAGES = PageTy(3, 'Campuses', index_locs, loc_builder)

see_department.init_handler(show_department)
