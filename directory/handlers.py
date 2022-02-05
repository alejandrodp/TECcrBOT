from telegram import Update
from telegram.ext import CallbackContext

from common.util import is_int, send_unknown_error
from directory.util import depts_builder


def show_department(update: Update, context: CallbackContext) -> None:
    unit_id = context.match.group(1)

    if not is_int(unit_id):
        send_unknown_error(update.effective_chat)
        return

    unit_id = int(unit_id)

    depts_builder(unit_id, update)
