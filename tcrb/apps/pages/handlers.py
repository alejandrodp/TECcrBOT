from enum import Enum

from telegram.ext import CallbackContext

from tcrb.apps.config.pages import show_page
from tcrb.core.buttons import InlineButton


class States(Enum):
    GET_PAGE = "get_page"


show_page_button = InlineButton("pages", States.GET_PAGE.value, r"(\d+)", r"(\d+)")


def build_show_page_button(text, ty, page_id):
    return show_page_button(text, ty, page_id)


def show_page_handler(reply, context: CallbackContext) -> None:
    ty = reply.expect_int(context.match.group(1))
    page_id = reply.expect_int(context.match.group(2))
    show_page(ty, page_id, reply)
