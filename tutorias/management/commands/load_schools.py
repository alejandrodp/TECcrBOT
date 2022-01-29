import json

import requests
from django.core.management.base import BaseCommand

from tutorias.models import School, Course


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        schools_data = requests.post(
                url='https://tec-appsext.itcr.ac.cr/guiahorarios/escuela.aspx/cargaEscuelas',
                headers={'Content-Type': 'application/json',
                         'Accept': 'application/json, text/javascript, */*; q=0.01'},
                verify=False
        )

        if schools_data.status_code == 200:
            schools = json.loads(schools_data.json()['d'])

            for sc in schools:

                courses_data = requests.post(
                    url='https://tec-appsext.itcr.ac.cr/guiahorarios/escuela.aspx/getdatosEscuelaAno',
                    json={'escuela': sc['IDE_DEPTO'], 'ano': '2022'},
                    headers={'Content-Type': 'application/json',
                             'Accept': 'application/json, text/javascript, */*; q=0.01'},
                    verify=False
                )

                if courses_data.status_code == 200:
                    courses = courses_data.json()['d']

                    if courses != 'NO DATOS':

                        s = School(name=sc['DSC_DEPTO'])

                        print(f"\nIngresando escuela: {sc['DSC_DEPTO']}")

                        s.save()

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
                        print(f'No hay cursos disponibles para {sc["DSC_DEPTO"]}')
                else:
                    print(f'No se pudo obtener los cursos para {sc["DSC_DEPTO"]}')
        else:
            print('No se pudo obtener las escuelas')
