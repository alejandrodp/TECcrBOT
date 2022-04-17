from django.conf import settings
from telegram import ParseMode
from telegram.ext import Updater, Defaults

from tcrb.apps.app_handlers import apps

defaults = Defaults(parse_mode=ParseMode.HTML, )


def start_polling():
    updater = Updater(token=settings.BOT_SECRET_KEY, defaults=defaults)
    dispatcher = updater.dispatcher
    _init_handlers(dispatcher)
    return updater.start_polling()


def _init_handlers(dispatcher) -> None:
    for group, handlers in apps.handlers.items():
        for handler in handlers:
            dispatcher.add_handler(handler, group)
