from telegram.ext import CallbackContext

from common.util import Reply
from directory.models import Unit
from directory.util import depts_page_builder, dept_text_builder, dept_people_paginator_builder


def show_department(reply: Reply, context: CallbackContext) -> None:
    unit_id = reply.expect_int(context.match.group(1))
    depts_page_builder(unit_id, reply)


def depts_people_pagination(reply: Reply, context: CallbackContext) -> None:
    current_page = reply.expect_int(context.match.group(1))
    unit_id = reply.expect_int(context.match.group(2))

    dept = Unit.objects.get(id=unit_id)
    msg = dept_text_builder(dept)
    paginator = dept_people_paginator_builder(current_page, dept)

    reply.text(msg, reply_markup=paginator.markup)
