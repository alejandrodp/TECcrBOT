import html

from telegram import Update, ReplyKeyboardMarkup, CallbackQuery
from telegram.ext import CallbackContext
from whoosh.searching import TimeLimit

from bot.buttons import page_button, one_type_paginator, type_selection_button, multiple_types_paginator
from bot.index import read_index, search
from common.util import is_int, send_unknown_error, send_text
from tcrb.core import BotAppConfig, PageTy

page_tys = PageTy.read_page_tys()


def main_menu(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Seleccione una opción:",
        reply_markup=ReplyKeyboardMarkup(
            BotAppConfig.get_main_menu(),
            resize_keyboard=True,
        )
    )


def show_page_handler(update: Update, context: CallbackContext) -> None:
    ty = context.match.group(1)
    page_id = context.match.group(2)
    update.callback_query.answer()

    if not is_int(ty, page_id):
        send_unknown_error(update.effective_chat)

    ty = int(ty)
    page_id = int(page_id)

    PageTy.show_page(page_id, ty, update)


def search_handler(update: Update, context: CallbackContext) -> None:
    query = html.escape(update.message.text)

    return search_query(query, reply_results, search_time_limit_error, update)


def search_query(query: str, callback, error_callback, update):
    with read_index() as ix:

        try:
            results = search(ix, query)
        except TimeLimit:
            error_callback(update)
            return

        docnums = {hit.docnum: hit for hit in results}
        hits = ((ty, [docnums.pop(no) for no in hits])
                for ty, hits in results.groups().items())

        groups = sorted(hits, key=lambda e: e[1][0].score, reverse=True)
        return callback(groups, update, query)


def search_time_limit_error(update: Update):
    update.effective_chat.send_message("Su búsqueda ha tardado demasiado, intente una búsqueda más simple")


def build_multiple_type_results(results, update, query, current_page):
    paginator = multiple_types_paginator.build_paginator(
        current_page,
        results,
        lambda pgs: (type_selection_button.build_button(f"{page_tys[ty].desc} ({len(pages)})", ty) for ty, pages in
                     pgs),
    )

    send_text(
        text=f"Se encontraron los siguientes resultadoss para <i>{query}</i>",
        update=update,
        reply_markup=paginator.markup
    )


def send_multiple_type_pages(update: Update, context: CallbackContext) -> None:
    cq = update.callback_query
    cq.answer()
    query = get_query(cq)

    def process_query(results: list, up, qu):
        current_page = context.match.group(1)

        if not is_int(current_page):
            send_unknown_error(update.effective_chat)
            return

        current_page = int(current_page)

        build_multiple_type_results(results, up, qu, current_page)

    search_query(query, process_query, search_time_limit_error, update)


def type_selection(update: Update, context: CallbackContext) -> None:
    cq = update.callback_query
    cq.answer()
    query = get_query(cq)
    ty = context.match.group(1)

    if not is_int(ty):
        send_unknown_error(update.effective_chat)

    ty = int(ty)

    def process_one_time_results(results: list, up, qu):

        for r_ty, pages in results:
            if r_ty == ty:
                build_one_type_results(ty, pages, up, qu, 1)

    search_query(query, process_one_time_results, search_time_limit_error, update)


def reply_results(results, update, query):
    match results:
        case []:
            update.message.reply_text(
                f'No se encontraron resultados para <i>{query}</i>')
        case [(ty, [page])]:
            page_tys[ty].page_builder(page["id"], update)
        case [(ty, pages)]:
            build_one_type_results(ty, pages, update, query, 1)
        case _:
            build_multiple_type_results(results, update, query, 1)


def send_one_type_page(update: Update, context: CallbackContext) -> None:
    cq = update.callback_query
    cq.answer()
    query = get_query(cq)

    def process_query(results: list, up, qu):
        current_page = context.match.group(1)
        ty = context.match.group(2)

        if not is_int(ty, current_page):
            send_unknown_error(update.effective_chat)
            return

        ty = int(ty)
        current_page = int(current_page)

        for r_ty, pages in results:
            if r_ty == ty:
                build_one_type_results(ty, pages, up, qu, current_page)

    search_query(query, process_query, search_time_limit_error, update)


def get_query(cq: CallbackQuery):
    ent = cq.message.entities[0]
    offset = ent.offset
    lenght = ent.offset + ent.length
    return html.escape(cq.message.text[offset:lenght])


def build_one_type_results(ty, pages, update, query, current_page):
    paginator = one_type_paginator.build_paginator(
        current_page,
        pages,
        lambda pgs: (page_button.build_button(page["title"], page["ty"], page["id"]) for page in pgs),
        ty
    )

    send_text(
        text=f"Se encontraron los siguientes resultados de {page_tys.get(ty).desc} para <i>{query}</i>",
        update=update,
        reply_markup=paginator.markup
    )
