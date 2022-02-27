from enum import Enum

from tcrb.apps.admin.config import AppConfig
from . import apps


class States(Enum):
    SEE_DEPARTMENT = "see_department"
    SEE_PEOPLE = "see_people"


config = AppConfig(apps.DirectoryConfig.name, apps.DirectoryConfig.verbose_name)

see_department = config.create_inline_button(States.SEE_DEPARTMENT, r"(\d+)")

department_people_paginator = config.create_paginator(States.SEE_PEOPLE, rf"(\d+)")
