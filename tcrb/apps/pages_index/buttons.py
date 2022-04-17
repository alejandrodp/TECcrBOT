from enum import Enum

from tcrb.core.buttons import InlinePaginator, InlineButton, InlineWhooshPaginator


class States(Enum):
    CHOOSING_PAGETY = "choosing_pagety"
    CHOOSING_PAGE = "choosing_page"
    SHOWING_PAGE = "showing_page"
    BACK_INDEX = "back"


pagety_button = InlineButton("pages_index", States.CHOOSING_PAGETY.value, rf"(\d+)")

pagesty_paginator = InlinePaginator(
    "pages_index",
    States.CHOOSING_PAGETY.value,
    lambda pgs: (pagety_button(page.desc, page.ty) for page in pgs)
)

pages_paginator = InlineWhooshPaginator("pages_index", States.SHOWING_PAGE.value, rf"(\d+)")

back_index = InlineButton("pages_index", States.BACK_INDEX.value)
