import os.path, subprocess, json

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction

from bot.models import Page
from directory.models import Person, Ty, Location, Unit, Role, RoleTy
from places.models import Place
import directory.settings
import places.settings

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
        ],
        capture_output = True
    ).stdout

    scrap = json.loads(str(scrap, 'utf-8'))

    for id, ty in enumerate(scrap['staff_types']):
        Ty(id = id, name = ty).save()

    locations = []
    for location in scrap['locations']:
        page = Page(ty = directory.settings.LOC_PAGES.ty)
        page.save()
        locations.append(page.id)

        Location(id = page.id, name = location['name'], href = location['href']).save()

    depts = []
    for unit in scrap['depts']:
        page = Page(ty = directory.settings.DEPT_PAGES.ty)
        page.save()
        depts.append(page.id)

        Unit(id = page.id, name = unit['name'], href = unit['href']).save()

    for person in scrap['staff']:
        page = Page(ty = directory.settings.PEOPLE_PAGES.ty)
        page.save()

        person_obj = Person(
            id = page.id,
            name = person['name'],
            surname = person['surname'],
            email = person.get('email'),
            phone = person.get('tel'),
            href = person['href'],
        )

        person_obj.save()

        for role in person.get('roles', ()):
            location = role.get('location')
            if location is not None:
                location = Location.objects.get(id = locations[location])

            unit_obj = Unit.objects.get(id = depts[role['dept']])
            role_obj = Role(person = person_obj, unit = unit_obj, location = location)
            role_obj.save()

            def insert_tys(key, is_function):
                for ty in role.get(key, ()):
                    ty_obj = Ty.objects.get(id = ty)
                    RoleTy(role = role_obj, ty = ty_obj, is_function = is_function).save()

            insert_tys('types', False)
            insert_tys('functions', True)

def load_places():
    with open(settings.BASE_DIR / 'contrib/places/places.json') as scrap:
        scrap = json.load(scrap)

    for place in scrap:
        page = Page(ty = places.settings.PLACE_PAGES.ty)
        page.save()

        photo = place.get('photo')
        if photo:
            photo = os.path.join('contrib/places/photos', photo)

        Place(
            id = page.id,
            name = place['name'],
            latitude = place['lat'],
            longitude = place['long'],
            photo = photo,
        ).save()
