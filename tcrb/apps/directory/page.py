import itertools

from telegram import InlineKeyboardMarkup

from .models import Person, Unit, Role, RoleTy, Location
from ...pages import build_show_page_button, PageTy


def index_people(person: Person):
    return {
        'kw': person_kws(person),
        'name': person.name,
        'surname': person.surname,
        'tel': person.phone,
        'email': person.email,
    }


def person_kws(person):
    from tcrb.apps.search import index
    return [kw.text
            for role in Role.objects.filter(person=person)
            for source in ((role.unit,), (role_ty.ty for role_ty in RoleTy.objects.filter(role=role)))
            for term in source
            for kw in index.HINT_ANALYZER(term.name)]


def loc_builder(location: Location, reply):
    reply.text(href(location))


def dept_builder(dept: Unit, reply):
    from .buttons import dept_people_paginator

    reply.text(href(dept),
               reply_markup=dept_people_paginator(1,
                                                  [role.person for role in dept.role_set.all()],
                                                  dept.id).markup)


def people_builder(person: Person, reply) -> None:
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

    def msg():
        yield f'Correo electrónico: {or_unavailable(person.email)}'
        yield f'Teléfono: {or_unavailable(person.phone)}'

        for role in person.role_set.all():
            yield ''
            yield from role_msg(role)

        yield ''
        yield href(person)

    reply.text('\n'.join(msg()),
               # TODO: Cambiar por sistema de enlazado general
               reply_markup=InlineKeyboardMarkup.from_column(list(
                   build_show_page_button(f"Ver {role.unit.name}", DEPT_PAGES.ty, role.unit.id)
                   for role in person.role_set.all()
               ))
               )


def or_unavailable(text, *, key=lambda x: x):
    return key(text) if text else 'No disponible'


def href(obj):
    return f'<a href="https://www.tec.ac.cr{obj.href}">Ver más información</a>'


PEOPLE_PAGES = PageTy(ty=1, model=Person,
                      desc='Personas', index=index_people, build=people_builder)

DEPT_PAGES = PageTy(ty=2, model=Unit, desc='Departamentos', build=dept_builder)

LOC_PAGES = PageTy(ty=3, model=Location, desc='Campuses', build=loc_builder)
