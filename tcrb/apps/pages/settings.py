from tcrb.apps.pages.handlers import show_page_button, show_page_handler
from tcrb.core.apps import HandlerConfig
from tcrb.core.apps.handlers.callbackquery import CallbackQueryHandler

PAGE_HANDLER_CONFIGS = HandlerConfig([
    CallbackQueryHandler(show_page_button, show_page_handler)
])
