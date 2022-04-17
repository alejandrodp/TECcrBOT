from telegram.ext import Filters

from tcrb.apps.tracking.handlers import query_track_handler
from tcrb.core.handlers import HandlerConfig, MessageHandler

TRACKING_HANDLERS = HandlerConfig([
    MessageHandler(Filters.text &
                   ~Filters.update.edited_message,
                   query_track_handler)
], 1)
