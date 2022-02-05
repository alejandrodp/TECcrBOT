from places.apps import PlacesConfig
from places.constants import States
from tcrb.core import BotAppConfig

config = BotAppConfig(PlacesConfig.name, PlacesConfig.verbose_name)

list_categories = config.create_inline_button(States.CHOOSING_CATEGORY)
list_categories_paginator = config.create_paginator(States.CHOOSING_CATEGORY)

list_places = config.create_inline_button(States.CHOOSING_PLACE, rf"(\d+)")
list_places_paginator = config.create_paginator(States.CHOOSING_PLACE, rf"(\d+)")
