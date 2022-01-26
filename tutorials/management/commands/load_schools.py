from time import sleep

from django.core.management.base import BaseCommand
import json

from django.db import IntegrityError

from places.models import Place, Location

import requests

from tutorials.models import School, Course


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        schools = json.loads(requests.post(
                url='https://tec-appsext.itcr.ac.cr/guiahorarios/escuela.aspx/cargaEscuelas',
                headers={'Content-Type': 'application/json',
                         'Accept': 'application/json, text/javascript, */*; q=0.01'},
                verify=False
            ).json()['d'])

        for sc in schools:

            print(f"\nIngresando escuela: {sc['DSC_DEPTO']}")
            s = School(name=sc['DSC_DEPTO'])

            courses = requests.post(
                url='https://tec-appsext.itcr.ac.cr/guiahorarios/escuela.aspx/getdatosEscuelaAno',
                json={'escuela': sc['IDE_DEPTO'], 'ano': '2022'},
                headers={'Content-Type': 'application/json',
                         'Accept': 'application/json, text/javascript, */*; q=0.01'},
                verify=False
            ).json()['d']

            s.save()

            if courses != 'NO DATOS':

                courses = json.loads(courses)
                print(f"Ingresando {len(courses)} cursos")
                for i, c in enumerate(courses, 1):
                    print(f"Ingresando curso {i}/{len(courses)}", end='\r')
                    if Course.objects.filter(code=c['IDE_MATERIA']).exists():
                        continue
                    Course(
                        code=c['IDE_MATERIA'],
                        name=c['DSC_MATERIA'],
                        school=s
                    ).save()
                print()
            else:
                print('No hay cursos disponibles')
