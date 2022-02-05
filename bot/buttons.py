from bot.apps import BotConfig
from tcrb.core import BotAppConfig


config = BotAppConfig(BotConfig.name, "")
page_button = config.create_inline_button('get_page', r"(\d+)", r"(\d+)")