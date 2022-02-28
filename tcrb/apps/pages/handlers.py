from enum import Enum

from telegram.ext import CallbackContext

from tcrb.core.apps.buttons import InlineButton
from tcrb.core.apps.handlers.base import Reply
from tcrb.core.apps.pages import show_page


class States(Enum):
    GET_PAGE = "get_page"


show_page_button = InlineButton("pages", States.GET_PAGE.value, r"(\d+)", r"(\d+)")


def show_page_handler(reply: Reply, context: CallbackContext) -> None:
    ty = reply.expect_int(context.match.group(1))
    page_id = reply.expect_int(context.match.group(2))
    show_page(ty, page_id, reply)
