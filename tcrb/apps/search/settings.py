from telegram.ext import Filters

from tcrb.apps.config.handlers import HandlerConfig, MessageHandler
from tcrb.apps.search.handlers import search_handler

SEARCH_HANDLERS = HandlerConfig([
    MessageHandler(Filters.text &
                   ~Filters.command &
                   ~Filters.update.edited_message &
                   ~Filters.update.edited_channel_post, search_handler)
])
