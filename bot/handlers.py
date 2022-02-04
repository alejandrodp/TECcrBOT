import html

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from whoosh.searching import Results

from bot import apps
from bot.index import search, read_index
from bot.menu import read_main_menu, BotHandler, build_page_button
from bot.pages import read_page_tys

handlers = BotHandler(apps.BotConfig.name)
page_tys = read_page_tys()


def main_menu(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Seleccione una opción:",
        reply_markup=ReplyKeyboardMarkup(
            read_main_menu(),
            resize_keyboard=True,
        )
    )


def _search(query: str):
    results_map = {}
    with read_index() as ix:
        results: Results = search(ix, query)
        for r in results:
            results_map.setdefault(r['ty'], []).append((r['id'], r['title']))
    return results_map


def search_handler(update: Update, context: CallbackContext) -> None:
    msg = html.escape(update.message.text)

    results = _search(msg)

    if len(results) == 0:
        update.message.reply_text(
            f'No se encontraron resultados para <i>{msg}</i>')
        return

    if len(results) == 1:
        ty, pages = results.popitem()
        msg, page_buttons = page_tys[ty].page_builder(pages[0][0])

        update.message.reply_text(
            text=msg,
            reply_markup=InlineKeyboardMarkup.from_column(page_buttons)
            if page_buttons else None
        )
        return

    text, buttons = build_results_menu(results, msg)

    update.message.reply_text(
        text=text,
        reply_markup=InlineKeyboardMarkup.from_column(buttons)
    )


def build_results_menu(results, msg):
    if len(results) > 1:
        text = f'Resultados para <i>{msg}</i>'
        buttons = [
            handlers.build_inline_button(f'{page_tys[ty].desc} ({len(pages)})', 'get_type_pages', str(ty))
            for ty, pages in results.items()]
    else:
        ty, pages = results.popitem()
        text = f'Resultados de {page_tys[ty].desc} para <i>{msg}</i>'
        buttons = [
            build_page_button(f'{page[1]}', ty, page[0])
            for page in pages
        ]

    return text, buttons


def type_handler(update: Update, context: CallbackContext) -> None:
    cq = update.callback_query
    cq.answer()
    ent = cq.message.entities[0]
    offset = ent.offset
    lenght = ent.offset + ent.length
    query = html.escape(cq.message.text[offset:lenght])
    ty = int(context.match.group(1))

    results = _search(query)

    if len(results[ty]) == 1:
        page_id, _ = results[ty][0]
        _show_page(page_id, ty, update)
        return

    cq.message.edit_text(
        text=f'Resultados de {page_tys[ty].desc} para <i>{query}</i>',
        reply_markup=InlineKeyboardMarkup.from_column([
            build_page_button(page[1], str(ty), str(page[0]))
            for page in results[ty]
        ])
    )


def show_page(update: Update, context: CallbackContext) -> None:
    ty = int(context.match.group(1))
    page_id = int(context.match.group(2))
    update.callback_query.answer()

    _show_page(page_id, ty, update)


def _show_page(page_id, ty, update):
    page_tys[ty].page_builder(page_id, update)
