import itertools
from typing import List, Optional

from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup

from bot.buttons import page_button
from bot.index import LANGUAGE_ANALYZER
from common.util import Reply
from .buttons import department_people_paginator
from .constants import PEOPLE_TY, DEPT_TY
from .models import Person, Unit, Role, RoleTy, Location


def index_people(person: Person):
    return {
        'kw': person_kws(person),
        'name': person.name,
        'surname': person.surname,
        'tel': person.phone,
        'email': person.email,
    }


def person_kws(person):
    return [kw.text
            for role in Role.objects.filter(person=person)
            for source in ((role.unit,), (role_ty.ty for role_ty in RoleTy.objects.filter(role=role)))
            for term in source
            for kw in LANGUAGE_ANALYZER(term.name)]


def loc_builder(location: Location, reply: Reply):
    reply.text(href(location))


def depts_page_builder(dept: Unit, reply: Reply):
    paginator = dept_people_paginator_builder(1, dept)
    reply.text(dept_text_builder(dept), reply_markup=paginator.markup)


def dept_text_builder(dept: Unit):
    return href(dept)


def dept_people_paginator_builder(current_page, dept):
    def build_person_buttons(pages):
        return list(page_button.build_button(f"{p.name} {p.surname}", PEOPLE_TY, p.id)
                    for p in pages)

    return department_people_paginator.build_paginator(current_page,
                                                       list(
                                                           r.person for r in dept.role_set.all()),
                                                       build_person_buttons,
                                                       dept.id)


def people_builder(person: Person, reply: Reply) -> None:
    def role_msg(role):
        functions, types = '', ''
        groups = itertools.groupby(role.rolety_set.all(), lambda role_ty: role_ty.is_function)
        for is_function, group in groups:
            group = ', '.join(role_ty.ty.name for role_ty in group)
            if is_function:
                functions = group
            else:
                types = f' ({group})'

        yield f'<u>{role.unit.name}</u>{types}'
        if functions:
            yield functions

        location = or_unavailable(role.location, key=lambda loc: loc.name)
        yield f'Ubicación: {location}'

    def msg():
        yield f'Correo electrónico: {or_unavailable(person.email)}'
        yield f'Teléfono: {or_unavailable(person.phone)}'

        for role in person.role_set.all():
            yield ''
            yield from role_msg(role)

        yield ''
        yield href(person)

    reply.text(
        '\n'.join(msg()),
        reply_markup=InlineKeyboardMarkup.from_column(list(
            page_button.build_button(f"Ver {role.unit.name}", DEPT_TY, role.unit.id)
            for role in person.role_set.all()
        ))
    )


def or_unavailable(text, *, key=lambda x: x):
    return key(text) if text else 'No disponible'


def href(obj):
    return f'<a href="https://www.tec.ac.cr{obj.href}">Ver más información</a>'
