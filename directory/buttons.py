from enum import Enum

from directory import apps
from tcrb.core import BotAppConfig


class States(Enum):
    SEE_DEPARTMENT = "see_department"
    SEE_PEOPLE = "see_people"


config = BotAppConfig(apps.DirectoryConfig.name, apps.DirectoryConfig.verbose_name)

see_department = config.create_inline_button(States.SEE_DEPARTMENT, r"(\d+)")
