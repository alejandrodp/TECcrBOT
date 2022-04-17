import tcrb.core.handlers
import handlers
import buttons

PAGE_HANDLER_CONFIGS = tcrb.core.handlers.HandlerConfig([
    tcrb.core.handlers.CallbackQueryHandler(buttons.show_page_button, handlers.show_page_handler)
])
