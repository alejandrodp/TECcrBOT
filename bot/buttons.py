from tcrb.core import BotAppConfig

page_button = BotAppConfig("pages", "").create_inline_button('get_page', r"(\d+)", r"(\d+)")