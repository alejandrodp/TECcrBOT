import os.path, subprocess, json

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction

from bot.models import Page
from directory.models import Person, Ty, Location, Unit, Role, RoleTy
import directory.settings

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        load_all()

@transaction.atomic
def load_all():
    for clazz in (Page, Person, Ty, Location, Unit, Role, RoleTy):
        assert clazz.objects.count() == 0, 'This operation requires a db flush'

    scrap_dir = os.path.join(settings.BASE_DIR, 'webscrap/people')
    scrap = subprocess.run(
        [
            os.path.join(scrap_dir, 'tag_edit.py'),
            '-o',
            '/dev/stdout',
            '-f',
            os.path.join(scrap_dir, 'tec.json'),
            '-l',
            os.path.join(scrap_dir, 'log.json'),
            '--role',
            'replay',
        ],
        capture_output = True
    ).stdout

    scrap = json.loads(str(scrap, 'utf-8'))

    for id, location in enumerate(scrap['locations']):
        Location(id = id, name = location['name'], href = location['href']).save()

    for id, ty in enumerate(scrap['staff_types']):
        Ty(id = id, name = ty).save()

    for id, unit in enumerate(scrap['depts']):
        Unit(id = id, name = unit['name'], href = unit['href']).save()

    for id, unit in enumerate(scrap['depts']):
        Unit(id = id, name = unit['name'], href = unit['href']).save()

    for person in scrap['staff']:
        page = Page(ty = directory.settings.PAGE_TY)
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
            unit_obj = Unit.objects.get(id = role['dept'])
            role_obj = Role(person = person_obj, unit = unit_obj)
            role_obj.save()

            def insert_tys(key, is_function):
                for ty in role.get(key, ()):
                    ty_obj = Ty.objects.get(id = ty)
                    RoleTy(role = role_obj, ty = ty_obj, is_function = is_function).save()

            insert_tys('types', False)
            insert_tys('functions', True)
