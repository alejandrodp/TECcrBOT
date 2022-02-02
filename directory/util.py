from telegram import Message

from .models import Person, Unit, Location


def index_people():
    for person in Person.objects.all():
        yield {
            'id': person.id,
            'title': f'{person.surname}, {person.name}',
            'name': person.name,
            'surname': person.surname,
            'tel': person.phone,
            'email': person.email,
        }


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


def loc_builder(page: int, msg: Message) -> None:
    loc = Location.objects.get(id=page)

    msg.edit_text(
        text=f'Nombre: {loc.name}\n\n'
             f'<a href="https://www.tec.ac.cr/{loc.href}">Ver más información</a>',
    )


def depts_builder(page: int, msg: Message) -> None:

    dept = Unit.objects.get(id=page)

    msg.edit_text(
        text=f'Nombre: {dept.name}\n\n'
             f'<a href="https://www.tec.ac.cr/{dept.href}">Ver más información</a>',
    )


def people_builder(page: int, msg: Message) -> None:

    person = Person.objects.get(id=page)

    email = person.email if person.email else 'No disponible'
    tel = person.phone if person.phone else 'No disponible'
    roles = '\n\n'.join([
        f'Departamento: {r.unit.name}\n'
        f'Funciones: {", ".join([n.ty.name for n in r.rolety_set.all()])}\n'
        f'Ubicación: {r.location.name if r.location else "No disponible"}\n'
        for r in person.role_set.all()
    ])


    msg.edit_text(
        text=f'Nombre: {person.name} {person.surname}\n'
             f'Correo electrónico: {email}\n'
             f'Teléfono: {tel}\n\n'
             f'{roles}\n'
             f'<a href="https://www.tec.ac.cr/{person.href}">Ver más información</a>',


    )
