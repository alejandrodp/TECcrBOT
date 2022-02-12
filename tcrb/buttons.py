from enum import Enum

from .apps import BotConfig
from .core import BotAppConfig


class States(Enum):
    GET_PAGE = "get_page"
    ONE_TYPE_RESULTS = "one_type_results"
    MULTIPLE_TYPE_RESULTS = "multi_type_results"


config = BotAppConfig(BotConfig.name, "Info️ \U00002139")
page_button = config.create_inline_button(States.GET_PAGE, r"(\d+)", r"(\d+)")

one_type_paginator = config.create_paginator(States.ONE_TYPE_RESULTS, rf"(\d+)")

multiple_types_paginator = config.create_paginator(States.MULTIPLE_TYPE_RESULTS)

type_selection_button = config.create_inline_button(States.MULTIPLE_TYPE_RESULTS, rf"(\d+)")
