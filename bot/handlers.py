import html

from telegram import Update, ReplyKeyboardMarkup, CallbackQuery
from telegram.ext import CallbackContext
from whoosh.searching import TimeLimit

from bot.buttons import page_button, one_type_paginator, type_selection_button, multiple_types_paginator
from bot.index import read_index, search
from common.util import Reply
from tcrb.core import BotAppConfig, PageTy

page_tys = PageTy.read_page_tys()


def main_menu(update: Update, context: CallbackContext) -> None:
    with Reply(update) as reply:
        reply.text(
            "Seleccione una opción:",
            reply_markup=ReplyKeyboardMarkup(
                BotAppConfig.get_main_menu(),
                resize_keyboard=True,
            )
        )


def show_page_handler(update: Update, context: CallbackContext) -> None:
    with Reply(update) as reply:
        ty = context.match.group(1)
        page_id = context.match.group(2)

        PageTy.show_page(int(page_id), int(ty), reply)


def search_handler(update: Update, context: CallbackContext) -> None:
    with Reply(update) as reply:
        return search_query(reply.text_query(), reply_results, search_time_limit_error, reply)


def search_query(query: str, callback, error_callback, reply):
    with read_index() as ix:
        try:
            results = search(ix, query)
        except TimeLimit:
            error_callback(reply)
            return

        docnums = {hit.docnum: hit for hit in results}
        hits = ((ty, [docnums.pop(no) for no in hits])
                for ty, hits in results.groups().items())

        groups = sorted(hits, key=lambda e: e[1][0].score, reverse=True)
        return callback(groups, reply, query)


def search_time_limit_error(reply: Reply):
    reply.text("Su búsqueda ha tardado demasiado, intente una búsqueda más simple")


def build_multiple_type_results(results, reply, query, current_page):
    paginator = multiple_types_paginator.build_paginator(
        current_page,
        results,
        lambda pgs: (type_selection_button.build_button(f"{page_tys[ty].desc} ({len(pages)})", ty) for ty, pages in
                     pgs),
    )

    reply.text(
        f"Se encontraron los siguientes resultadoss para <i>{html.escape(query)}</i>",
        reply_markup=paginator.markup
    )


def send_multiple_type_pages_handler(update: Update, context: CallbackContext) -> None:
    with Reply(update) as reply:
        query = get_query(reply.callback_query())

        def process_query(results: list, up, qu):
            current_page = int(context.match.group(1))
            build_multiple_type_results(results, up, qu, current_page)

        search_query(query, process_query, search_time_limit_error, reply)


def type_selection_handler(update: Update, context: CallbackContext) -> None:
    with Reply(update) as reply:
        query = get_query(reply.callback_query())
        ty = int(context.match.group(1))

        def process_one_time_results(results: list, up, qu):
            for r_ty, pages in results:
                if r_ty == ty:
                    build_one_type_results(ty, pages, up, qu, 1)

        search_query(query, process_one_time_results,
                     search_time_limit_error, reply)


def reply_results(results, reply, query):
    match results:
        case []:
            reply.text(
                f'No se encontraron resultados para <i>{html.escape(query)}</i>')
        case [(ty, [page])]:
            page_tys[ty].page_builder(page["id"], reply)
        case [(ty, pages)]:
            build_one_type_results(ty, pages, reply, query, 1)
        case _:
            build_multiple_type_results(results, reply, query, 1)


def send_one_type_page_handler(update: Update, context: CallbackContext) -> None:
    with Reply(update) as reply:
        query = get_query(reply.callback_query())

        def process_query(results: list, up, qu):
            current_page = int(context.match.group(1))
            ty = int(context.match.group(2))

            for r_ty, pages in results:
                if r_ty == ty:
                    build_one_type_results(ty, pages, up, qu, current_page)

        search_query(query, process_query, search_time_limit_error, reply)


def get_query(cq: CallbackQuery):
    ent = cq.message.entities[0]
    offset = ent.offset
    lenght = ent.offset + ent.length
    return cq.message.text[offset:lenght]


def build_one_type_results(ty, pages, reply, query, current_page):
    paginator = one_type_paginator.build_paginator(
        current_page,
        pages,
        lambda pgs: (page_button.build_button(
            page["title"], page["ty"], page["id"]) for page in pgs),
        ty
    )

    desc = page_tys.get(ty).desc
    text = f"Se encontraron los siguientes resultados de {desc} para <i>{html.escape(query)}</i>"

    reply.text(text, reply_markup=paginator.markup)
