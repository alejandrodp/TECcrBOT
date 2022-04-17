from tcrb.apps.pages.handlers import show_page_handler, show_page_button
from tcrb.core.handlers import HandlerConfig, CallbackQueryHandler

PAGE_HANDLER_CONFIGS = HandlerConfig([
    CallbackQueryHandler(show_page_button, show_page_handler)
])
