import json

import requests
from bs4 import BeautifulSoup

import urllib3

urllib3.disable_warnings()

YEAR = "2022"
SEMESTER = "1"
ROOT = "https://tecdigital.tec.ac.cr"
KEY = "key"
DATA = "data"

session = requests.Session()


def load(url, **kwargs):
    data = session.get(
        url=url,
        verify=False,
        **kwargs
    )
    data.raise_for_status()
    if data.status_code == 200:
        return data.json()


locations = load(url=f"{ROOT}/tds-curriculum-exp/ajax/carga_sedes_json")["sedes"]


def load_periods():
    all_periods = load(url=f"{ROOT}/tda-expediente-estudiantil/ajax/combos/carga_periodos_tds_lib")
    return list(filter(lambda period: all(good_token in period["key"]
                                          for good_token in (YEAR, f"_{SEMESTER}"))
                                      and
                                      all(bad_token not in period[KEY]
                                          for bad_token in ("V", "H")), all_periods))


periods = load_periods()


def load_schools(location):
    return load(url=f"{ROOT}/tds-curriculum-exp/ajax/carga_carreras_json?id_sede={location}")["carreras"]


def load_courses(location, school, period):
    courses = session.post(
        url=f"{ROOT}/tda-expediente-estudiantil/ajax/tabla_guia_horario",
        verify=False,
        data={
            "sede": location,
            "carrera": school,
            "periodo": period
        }
    )
    courses.raise_for_status()

    if courses.status_code == 200:
        table_data = BeautifulSoup(courses.text, features="lxml")

        courses = [[cell.text for cell in row("td")]
                   for row in table_data("tr")]

        match courses:
            case [[error]]:
                return None
            case _:
                return [(course[0], course[1]) for course in courses]


schools = {}
courses = {}
new_locations = {}

if __name__ == '__main__':
    for location in locations:
        loc_id = location[KEY]
        for school in load_schools(loc_id):
            school_id = school[KEY]
            for period in periods:
                sc_courses = load_courses(loc_id, school_id, period[KEY])
                if sc_courses:
                    print(f"Sede: {location[DATA]}\n"
                          f"Escuela: {school[DATA]}\n"
                          f"Periodo: {period[DATA]}\n"
                          f"Cursos: {sc_courses}", end="\n\n")
                    schools.setdefault(school_id, school[DATA])
                    new_locations.setdefault(loc_id, location[DATA])
                    for code, name in sc_courses:
                        courses.setdefault(code, name)

    data = {
        "locations": new_locations,
        "schools": schools,
        "courses": courses
    }

    with open("data.json", "w") as fp:
        json.dump(data, fp, indent=4)
