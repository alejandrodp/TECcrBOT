from bot.pages import PageTy
from .util import index_people, index_depts, index_locs

HANDLERS = []

PEOPLE_PAGES = PageTy(1, 'Personas', index_people)
DEPT_PAGES = PageTy(2, 'Departamentos', index_depts)
LOC_PAGES = PageTy(3, 'Campuses', index_locs)
