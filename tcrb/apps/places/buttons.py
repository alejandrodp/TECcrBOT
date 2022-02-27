from tcrb.apps.config import BotAppConfig
from .apps import PlacesConfig

config = BotAppConfig(PlacesConfig.name, PlacesConfig.verbose_name)
