import os.path, datetime, subprocess, json

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction

from bot.models import Page
from directory.models import Person, Ty, Location, Unit, Role, RoleTy
from transportation.models import Place as T_place, Vehicle, Route, Stop, Schedule
from places.models import Place
from directory.settings import LOC_PAGES, DEPT_PAGES, PEOPLE_PAGES
from places.settings import PLACE_PAGES
from transportation.settings import ROUTE_PAGES

from datetime import time


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        load_all()


@transaction.atomic
def load_all():
    for clazz in (Page, Person, Ty, Location, Unit, Role, RoleTy, Place, T_place, Vehicle, Route, Stop, Schedule):
        assert clazz.objects.count() == 0, 'This operation requires a db flush'

    load_people()
    load_places()
    load_transportation()


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
        id = new_page(LOC_PAGES)

        locations.append(id)
        Location(id=id, name=location['name'],
                 href=location['href']).save()

    depts = []
    for unit in scrap['depts']:
        id = new_page(DEPT_PAGES)

        depts.append(id)
        Unit(id=id, name=unit['name'], href=unit['href']).save()

    for person in scrap['staff']:
        person_obj = Person(
            id=new_page(PEOPLE_PAGES),
            name=person['name'],
            surname=person['surname'],
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
        photo = place.get('photo')
        if photo:
            photo = os.path.join('contrib/places/photos', photo)

        Place(
            id=new_page(PLACE_PAGES),
            name=place['name'],
            latitude=place['lat'],
            longitude=place['long'],
            photo=photo,
        ).save()


def load_transportation():
    with open(settings.BASE_DIR / 'contrib/transportation/transportation.json') as scrap:
        scrap = json.load(scrap)

    for route in scrap:
        target_route = Route(
            id=new_page(ROUTE_PAGES, mtime=datetime.date.fromisoformat(route['mtime'])),
            source=T_place.objects.get_or_create(name=route["src"].title())[0],
            destination=T_place.objects.get_or_create(name=route["dest"].title())[0],
            vehicle=Vehicle.objects.get_or_create(name=route["vehicle"])[0],
            price=route["price"]
        )

        target_route.save()

        for stop in route["stops"]:
            if "time" not in stop:
                Stop(
                    route=target_route,
                    address=stop["address"],
                    terminus=stop["terminus"]
                ).save()
            else:
                for tm in stop["time"]:
                    Stop(
                        route=target_route,
                        time=tm,
                        address=stop["address"],
                        terminus=stop["terminus"]
                    ).save()

def new_page(page_ty, *, mtime=None):
    page = Page(ty=page_ty.ty, mtime=mtime)
    page.save()

    return page.id
