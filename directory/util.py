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
