from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

from bot.settings import MAIN_MENU


def main_menu(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Seleccione una opción:",
        reply_markup=ReplyKeyboardMarkup(
            MAIN_MENU,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )
