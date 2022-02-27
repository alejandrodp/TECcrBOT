from tcrb.apps.config import PageTy, BotAppConfig
from . import apps
from .handlers import main_entry
from .models import Service
from .util import service_builder


config = BotAppConfig(apps.ServicesConfig.name, apps.ServicesConfig.verbose_name)

config.add_main_menu_entry(main_entry)

SERVICES_PAGE = PageTy(ty=0, model=Service, desc=apps.ServicesConfig.verbose_name, build=service_builder)
