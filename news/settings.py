from telegram.ext import MessageHandler, Filters

from news.handlers import main_entry

MAIN_MENU_COMMAND = 'Noticias TEC 📰'


HANDLERS = [
    MessageHandler(Filters.text(MAIN_MENU_COMMAND), main_entry)
]
