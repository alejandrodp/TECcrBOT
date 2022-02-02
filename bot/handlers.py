from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from whoosh.query import Query

from bot import apps
from bot.index import search, read_index
from bot.pages import read_page_tys
from bot.settings import MAIN_MENU

IKB = InlineKeyboardButton


def main_menu(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Seleccione una opción:",
        reply_markup=ReplyKeyboardMarkup(
            MAIN_MENU,
            resize_keyboard=True,
        )
    )


def search_handler(update: Update, context: CallbackContext) -> None:
    msg = update.message.text

    tys = {}

    with read_index() as ix:
        results = search(ix, msg)

        for r in results:
            if not tys.get(r['ty']):
                tys[r['ty']] = [r['id']]
            else:
                tys[r['ty']].append(r['id'])

        update.message.reply_text(
            text=f'Resultados para <i>{msg}</i>',
            reply_markup=InlineKeyboardMarkup.from_column([
                IKB(f'{read_page_tys()[ty].desc} ({len(ids)})', callback_data=f'{apps.BotConfig.name}:get_type_pages:{ty}')
                for ty, ids in tys.items()
            ])
        )


def type_handler(update: Update, context: CallbackContext) -> None:
    cq = update.callback_query
    cq.answer()
    ent = cq.message.entities[0]
    offset = ent.offset
    lenght = ent.offset + ent.length
    query = cq.message.text[offset:lenght]
    ty = int(context.match.group(1))

    with read_index() as ix:
        results = search(ix, query)

        cq.message.edit_text(
            text=f'Resultados de {read_page_tys()[ty].desc} para <i>{query}</i>',
            reply_markup=InlineKeyboardMarkup.from_column([
                IKB(r['title'], callback_data=f'{apps.BotConfig.name}:get_page:{r["id"]}')
                for r in results if r['ty'] == ty
            ])
        )
