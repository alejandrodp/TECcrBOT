from enum import Enum

from tcrb.core.buttons import InlineButton


class States(Enum):
    GET_PAGE = "get_page"


show_page_button = InlineButton("pages", States.GET_PAGE.value, r"(\d+)", r"(\d+)")


def build_show_page_button(text, ty, page_id):
    return show_page_button(text, ty, page_id)
