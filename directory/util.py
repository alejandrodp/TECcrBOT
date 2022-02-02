from .models import Person


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
