from telegram.ext import Filters

from tcrb.apps.config.handlers import HandlerConfig, MessageHandler, CallbackQueryHandler
from tcrb.apps.search.buttons import one_type_results_paginator, page_ty_result
from tcrb.apps.search.handlers import search_handler, one_type_results_paginator_handler, page_ty_result_handler

SEARCH_HANDLERS = HandlerConfig([
    CallbackQueryHandler(one_type_results_paginator, one_type_results_paginator_handler),
    CallbackQueryHandler(page_ty_result, page_ty_result_handler),
    MessageHandler(Filters.text &
                   ~Filters.command &
                   ~Filters.update.edited_message &
                   ~Filters.update.edited_channel_post, search_handler)
])
