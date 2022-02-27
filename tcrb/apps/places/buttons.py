from tcrb.apps.admin.config import AppConfig
from .apps import PlacesConfig

config = AppConfig(PlacesConfig.name, PlacesConfig.verbose_name)
