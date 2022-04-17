from enum import Enum

from tcrb.apps.directory import settings
from tcrb.core.buttons import InlinePaginator
from tcrb.pages import build_show_page_button


class States(Enum):
    SHOWING_DEPARTMENT = "showing_dept"


dept_people_paginator = InlinePaginator(
    "directory",
    States.SHOWING_DEPARTMENT.value,
    lambda pages: [build_show_page_button(f"{person.name} {person.surname}", settings.PEOPLE_PAGES.ty, person.id)
                   for person in pages],
    rf"(\d+)"
)
