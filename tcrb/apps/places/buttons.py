from tcrb.core.apps import HandlerConfig
from .apps import PlacesConfig

config = HandlerConfig(PlacesConfig.name, PlacesConfig.verbose_name)
