from telegram.ext import Filters

from tcrb.apps.config.handlers import HandlerConfig, MessageHandler
from tcrb.apps.search.handlers import search_handler

SEARCH_HANDLERS = HandlerConfig([
    MessageHandler(Filters.text & ~Filters.command, search_handler)
])
