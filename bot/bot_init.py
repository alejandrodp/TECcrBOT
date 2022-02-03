from queue import Queue
from typing import Optional

from django.conf import settings
from telegram import ParseMode
from telegram.ext import Updater, Dispatcher, CommandHandler, Defaults, Handler, MessageHandler, Filters, \
    CallbackQueryHandler

from bot import apps
from bot.settings import APP_CONFIGS
from bot.handlers import main_menu, type_handler, search_handler, show_page

defaults = Defaults(parse_mode=ParseMode.HTML, )


def start_polling() -> Optional[Queue]:

    updater = Updater(token=settings.BOT_SECRET_KEY, defaults=defaults)
    dispatcher = updater.dispatcher
    _init_handlers(dispatcher)
    return updater.start_polling()


def _add_default_handlers(dispatcher: Dispatcher):
    dispatcher.add_handler(CommandHandler("menu", main_menu))
    dispatcher.add_handler(CommandHandler("start", main_menu))
    dispatcher.add_handler(CallbackQueryHandler(
        type_handler, pattern=rf'{apps.BotConfig.name}:get_type_pages:(\d+)'))
    dispatcher.add_handler(CallbackQueryHandler(
        show_page, pattern=rf'{apps.BotConfig.name}:get_page:(\d+):(\d+)'))


def _init_handlers(dispatcher: Dispatcher) -> None:
    _add_default_handlers(dispatcher)

    for config in APP_CONFIGS.values():
        handlers: list = getattr(config, 'HANDLERS', None)
        for hdrl in handlers or ():
            dispatcher.add_handler(hdrl)

    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, search_handler))
