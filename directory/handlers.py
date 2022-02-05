from telegram import Update
from telegram.ext import CallbackContext

from common.util import is_int, send_unknown_error, send_text
from directory.models import Unit
from directory.util import depts_page_builder, dept_text_builder, dept_people_paginator_builder


def show_department(update: Update, context: CallbackContext) -> None:
    unit_id = context.match.group(1)

    if not is_int(unit_id):
        send_unknown_error(update.effective_chat)
        return

    unit_id = int(unit_id)

    depts_page_builder(unit_id, update)


def depts_people_pagination(update: Update, context: CallbackContext) -> None:
    current_page = context.match.group(1)
    unit_id = context.match.group(2)

    if not is_int(current_page, unit_id):
        send_unknown_error(update.effective_chat)
        return

    current_page = int(current_page)
    unit_id = int(unit_id)

    dept = Unit.objects.get(id=unit_id)

    msg = dept_text_builder(dept)

    paginator = dept_people_paginator_builder(current_page, dept)

    send_text(msg, update, reply_markup=paginator.markup)
