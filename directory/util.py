from typing import List, Optional

from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup

from bot.buttons import page_button
from bot.index import LANGUAGE_ANALYZER
from common.util import send_text
from .buttons import department_people_paginator
from .constants import PEOPLE_TY, DEPT_TY
from .models import Person, Unit, Role, RoleTy, Location


def index_people():
    for person in Person.objects.all():
        yield {
            'id': person.id,
            'title': f'{person.surname}, {person.name}',
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


def index_depts():
    for unit in Unit.objects.all():
        yield {
            'id': unit.id,
            'title': unit.name,
        }


def index_locs():
    for location in Location.objects.all():
        yield {
            'id': location.id,
            'title': location.name,
        }


def loc_builder(page: int, update: Update) -> (str, Optional[List[InlineKeyboardButton]]):
    loc = Location.objects.get(id=page)

    msg = f'Nombre: {loc.name}\n\n<a href="https://www.tec.ac.cr{loc.href}">Ver más información</a>'

    send_text(msg, update)


def depts_page_builder(page: int, update: Update) -> (str, Optional[List[InlineKeyboardButton]]):
    dept = Unit.objects.get(id=page)

    msg = dept_text_builder(dept)

    paginator = dept_people_paginator_builder(1, dept)

    send_text(msg, update, reply_markup=paginator.markup)


def dept_text_builder(dept):

    return f'Nombre: {dept.name}\n\n<a href="https://www.tec.ac.cr{dept.href}">Ver más información</a>'


def dept_people_paginator_builder(current_page, dept):
    def build_person_buttons(pages):
        return list(page_button.build_button(f"{p.name} {p.surname}", PEOPLE_TY, p.id)
                    for p in pages)

    return department_people_paginator.build_paginator(current_page,
                                                       list(r.person for r in dept.role_set.all()),
                                                       build_person_buttons,
                                                       dept.id)


def people_builder(page: int, update: Update) -> None:
    person = Person.objects.get(id=page)

    email = person.email if person.email else 'No disponible'
    tel = person.phone if person.phone else 'No disponible'

    roles = '\n\n'.join([
        f'Departamento: {r.unit.name}\n'
        f'Funciones: {", ".join([n.ty.name for n in r.rolety_set.all()]) if r.rolety_set.exists() else "No disponible"}\n'
        f'Ubicación: {r.location.name if r.location else "No disponible"}\n'
        for r in person.role_set.all()
    ])

    msg = f'Nombre: {person.name} {person.surname}\n' \
          f'Correo electrónico: {email}\n' \
          f'Teléfono: {tel}\n\n' \
          f'{roles}\n' \
          f'<a href="https://www.tec.ac.cr{person.href}">Ver más información</a>'

    send_text(
        msg,
        update,
        reply_markup=InlineKeyboardMarkup.from_column(list(set((
            page_button.build_button(f"Ver {r.unit.name}", DEPT_TY, r.unit.id)
            for r in person.role_set.all()
        ))))
    )
