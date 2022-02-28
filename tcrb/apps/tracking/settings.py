from telegram.ext import Filters

from tcrb.apps.config.handlers import HandlerConfig, MessageHandler
from tcrb.apps.tracking.handlers import query_track_handler

TRACKING_HANDLERS = HandlerConfig([
    MessageHandler(Filters.text &
                   ~Filters.update.edited_message,
                   query_track_handler)
], 1)
