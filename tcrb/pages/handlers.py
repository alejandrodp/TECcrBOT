from telegram.ext import CallbackContext


def show_page_handler(reply, context: CallbackContext) -> None:
    from .util import show_page
    ty = reply.expect_int(context.match.group(1))
    page_id = reply.expect_int(context.match.group(2))
    show_page(ty, page_id, reply)
