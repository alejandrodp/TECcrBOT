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
        ty = reply.expect_int(context.match.group(1))
        page_id = reply.expect_int(context.match.group(2))

        reply.expect_idx(page_tys, ty).page_builder(page_id, reply)


def search_handler(update: Update, context: CallbackContext) -> None:
    with Reply(update) as reply:
        query = reply.text_query()
        def reply_results(results):
            match results:
                case []:
                    reply.text(
                        f'No se encontraron resultados para <i>{html.escape(query)}</i>')
                case [(ty, [page])]:
                    reply.expect_idx(page_tys, ty).page_builder(page["id"], reply)
                case [(ty, pages)]:
                    build_one_type_results(ty, pages, reply, query, 1)
                case _:
                    build_multiple_type_results(results, reply, query, 1)

        return search_query(query, reply_results, reply)


def search_query(query: str, callback, reply):
    with read_index() as ix:
        try:
            results = search(ix, query)
        except TimeLimit:
            reply.fail("Su búsqueda ha tardado demasiado, intente una búsqueda más simple")

        docnums = {hit.docnum: hit for hit in results}
        hits = ((ty, [docnums.pop(no) for no in hits])
                for ty, hits in results.groups().items())

        groups = sorted(hits, key=lambda e: e[1][0].score, reverse=True)
        return callback(groups)


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
        current_page = reply.expect_int(context.match.group(1))

        def process_query(results: list):
            build_multiple_type_results(results, reply, query, current_page)

        search_query(query, process_query, reply)


def type_selection_handler(update: Update, context: CallbackContext) -> None:
    with Reply(update) as reply:
        query = get_query(reply.callback_query())
        ty = reply.expect_int(context.match.group(1))

        def process_one_time_results(results: list):
            for r_ty, pages in results:
                if r_ty == ty:
                    build_one_type_results(ty, pages, reply, query, 1)

        search_query(query, process_one_time_results, reply)


def send_one_type_page_handler(update: Update, context: CallbackContext) -> None:
    with Reply(update) as reply:
        query = get_query(reply.callback_query())

        current_page = reply.expect_int(context.match.group(1))
        ty = reply.expect_int(context.match.group(2))

        def process_query(results: list):
            for r_ty, pages in results:
                if r_ty == ty:
                    build_one_type_results(ty, pages, reply, query, current_page)

        search_query(query, process_query, reply)


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
