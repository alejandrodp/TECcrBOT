from django.core.management.base import BaseCommand
import json

from django.db import IntegrityError

from places.models import Place, Location


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        data = json.loads(open("/home/alejandro/projects/trcb-old/data/json/AEMTEC_TECCRbot_ubicaciones.json", "r").read())

        for elm in data:
            ubicacion = elm['ubicacion'].split(", ")

            nombre = elm['nombre']

            try:
                Location(
                    longitude=ubicacion[1],
                    latitude=ubicacion[0]).save()
            except IntegrityError:
                print(f"Ubicación repetida: {elm}")
                continue


            try:
                Place(
                    name=nombre,
                    location_id=Location.objects.get(latitude=ubicacion[0], longitude=ubicacion[1]).id
                ).save()
            except IntegrityError:
                print(f"Lugar con nombre repetido: {elm}")
                continue









