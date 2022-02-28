from telegram.ext import Filters

from tcrb.apps.search.handlers import search_handler
from tcrb.core.apps import HandlerConfig
from tcrb.core.apps.handlers import MessageHandler

SEARCH_HANDLERS = HandlerConfig([
    MessageHandler(Filters.text & ~Filters.command, search_handler)
])
