from tcrb.apps.directory.settings import PEOPLE_PAGES, DEPT_PAGES, LOC_PAGES
from tcrb.apps.places.settings import PLACES_PAGE
from tcrb.apps.services.settings import SERVICES_PAGE


class PageTys:
    def __init__(self, page_configs):
        self._page_tys = {}
        self._create_pages(page_configs)

    @property
    def page_tys(self):
        return self._page_tys

    def _create_pages(self, page_configs):
        for page in page_configs:
            existing = self._page_tys.get(page.ty)
            if existing:
                raise ValueError(f"Page type `{page.desc}` collides with `{existing.desc}`")
            self._page_tys[page.ty] = page


all_pages = PageTys([
    SERVICES_PAGE,
    PLACES_PAGE,
    PEOPLE_PAGES,
    DEPT_PAGES,
    LOC_PAGES,
])
