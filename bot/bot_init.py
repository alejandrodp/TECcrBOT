from queue import Queue
from typing import Optional

from django.conf import settings
from telegram import ParseMode
from telegram.ext import Updater, Dispatcher, Defaults

from bot.menu import BotHandler

defaults = Defaults(parse_mode=ParseMode.HTML, )


def start_polling() -> Optional[Queue]:

    updater = Updater(token=settings.BOT_SECRET_KEY, defaults=defaults)
    dispatcher = updater.dispatcher
    _init_handlers(dispatcher)
    return updater.start_polling()


def _init_handlers(dispatcher: Dispatcher) -> None:

    import bot.settings as _
    for handler in BotHandler._handlers:
        dispatcher.add_handler(handler)

