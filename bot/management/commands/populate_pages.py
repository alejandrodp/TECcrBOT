import json
import os.path
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from bot.models import Page
from directory.models import Person, Ty, Location, Unit, Role, RoleTy
from directory.settings import LOC_PAGES, DEPT_PAGES, PEOPLE_PAGES
from places.models import Place
from places.settings import PLACE_PAGES


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        load_all()


@transaction.atomic
def load_all():
    for clazz in (Page, Person, Ty, Location, Unit, Role, RoleTy, Place):
        assert clazz.objects.count() == 0, 'This operation requires a db flush'

    load_people()
    load_places()


def load_people():
    scrap_dir = settings.BASE_DIR / 'contrib/people'
    scrap = subprocess.run(
        [
            scrap_dir / 'tag_edit.py',
            '-o',
            '/dev/stdout',
            '-f',
            scrap_dir / 'tec.json',
            '-l',
            scrap_dir / 'log.json',
            '--role',
            'replay',
            '--compact'
        ],
        capture_output=True
    ).stdout

    scrap = json.loads(str(scrap, 'utf-8'))

    for id, ty in enumerate(scrap['staff_types']):
        Ty(id=id, name=ty).save()

    locations = []
    for location in scrap['locations']:
        name = location['name']
        id = new_page(LOC_PAGES, title=name)

        locations.append(id)
        Location(id=id, name=name, href=location['href']).save()

    depts = []
    for unit in scrap['depts']:
        name = unit['name']
        id = new_page(DEPT_PAGES, title=name)

        depts.append(id)
        Unit(id=id, name=name, href=unit['href']).save()

    for person in scrap['staff']:
        name, surname = person['name'], person['surname']
        person_obj = Person(
            id=new_page(PEOPLE_PAGES, title=f'{surname}, {name}'),
            name=name,
            surname=surname,
            email=person.get('email'),
            phone=person.get('tel'),
            href=person['href'],
        )

        person_obj.save()

        for role in person.get('roles', ()):
            location = role.get('location')
            if location is not None:
                location = Location.objects.get(id=locations[location])

            unit_obj = Unit.objects.get(id=depts[role['dept']])
            role_obj = Role(person=person_obj,
                            unit=unit_obj, location=location)
            role_obj.save()

            def insert_tys(key, is_function):
                for ty in role.get(key, ()):
                    ty_obj = Ty.objects.get(id=ty)
                    RoleTy(role=role_obj, ty=ty_obj,
                           is_function=is_function).save()

            insert_tys('types', False)
            insert_tys('functions', True)


def load_places():
    with open(settings.BASE_DIR / 'contrib/places/places.json') as scrap:
        scrap = json.load(scrap)

    for place in scrap:
        name = place['name']
        photo = place.get('photo')
        if photo:
            photo = os.path.join('contrib/places/photos', photo)

        Place(
            id=new_page(PLACE_PAGES, title=name),
            name=name,
            latitude=place['lat'],
            longitude=place['long'],
            photo=photo,
        ).save()


def new_page(page_ty, *, title, mtime=None):
    page = Page(ty=page_ty.ty, title=title, mtime=mtime)
    page.save()

    return page.id
