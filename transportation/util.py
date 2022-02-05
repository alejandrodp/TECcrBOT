from telegram import Update
from whoosh.searching import Hit
from typing import List, Optional

from .models import Route, Stop
import itertools


def index_route():
    for route in Route.objects.all():
        yield {
            'id': route.id,
            'title': f'Ruta en {route.vehicle.name}: {route.source.name} - {route.destination.name}'
        }


def route_builder(page: Hit, update: Update):

    route = Route.objects.get(id=page["id"])

    render_route(route)


def render_route(route):
    all_stops = Stop.objects.filter(route_id=route.id).order_by("terminus")
    departures = []
    stops = []

    for terminus, stop in itertools.groupby(all_stops, key=lambda stop: stop.terminus):
        (stops if terminus else departures).extend(stop)

    return "La ruta {src} - {dest} cuesta {price}.\n" \
               "Sale de:\n" \
               "{deps}\n" \
               "De Lunes a Viernes pasa por:\n" \
               "{stps}\n".format(
        src=route.source,
        dest=route.destination,
        price=route.price,
        deps="\n".join(f"{dep.address} a las {dep.time}" for dep in departures),
        stps="\n".join(f"{stp.address} a las {stp.time}" for stp in stops)
    )
