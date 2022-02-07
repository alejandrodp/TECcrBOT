from places.apps import PlacesConfig
from tcrb.core import BotAppConfig

config = BotAppConfig(PlacesConfig.name, PlacesConfig.verbose_name)
