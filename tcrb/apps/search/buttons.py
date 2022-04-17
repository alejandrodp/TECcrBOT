from enum import Enum

from tcrb.apps.pages.handlers import build_show_page_button
from tcrb.core.buttons import InlinePaginator, InlineButton


class Results(Enum):
    ONE_TYPE = "one_type"
    MULTIPLE_TYPES = "multiple_types"


one_type_results_paginator = InlinePaginator(
    "search",
    Results.ONE_TYPE.value,
    lambda pgs: (build_show_page_button(page["title"], page["ty"], page["id"]) for page in pgs),
    rf"(\d+)"
)

page_ty_result = InlineButton("search", Results.MULTIPLE_TYPES.value, rf"(\d+)")
