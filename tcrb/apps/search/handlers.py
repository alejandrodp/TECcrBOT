from telegram.ext import CallbackContext, Filters

from tcrb.apps.search.buttons import one_type_results_paginator, page_ty_result
from tcrb.apps.search.queries import search_query, clean_query, build_query, get_query
from tcrb.apps.search.results import show_one_type_results, show_multiple_results
from tcrb.core.handlers import HandlerConfig, CallbackQueryHandler, MessageHandler
from tcrb.pages import show_page


def search_handler(reply, context: CallbackContext) -> None:
    query = clean_query(reply.text_query())

    def reply_results(results):
        match results:
            case []:
                reply.text(f'No se encontraron resultados para {build_query(query)}\n\n')
            case [(ty, [result])]:
                show_page(ty, result['id'], reply)
            case [(ty, results)]:
                show_one_type_results(ty, results, query, reply)
            case _:
                show_multiple_results(results, query, reply)

    return search_query(query, reply_results, reply)


def one_type_results_paginator_handler(reply, context: CallbackContext) -> None:
    query = get_query(reply.text_query())

    current_page = reply.expect_int(context.match.group(1))
    ty = reply.expect_int(context.match.group(2))

    def process_query(results: list):
        for r_ty, pages in results:
            if r_ty == ty:
                paginator = one_type_results_paginator(current_page, pages, ty)
                reply.edit_markup(paginator.markup)

    search_query(query, process_query, reply)


def page_ty_result_handler(reply, context: CallbackContext) -> None:
    ty = reply.expect_int(context.match.group(1))
    query = get_query(reply.text_query())

    def process_query(results: list):
        for r_ty, pages in results:
            if r_ty == ty:
                if len(pages) == 1:
                    show_page(r_ty, pages[0]["id"], reply)
                    return
                show_one_type_results(r_ty, pages, query, reply)

    search_query(query, process_query, reply)


def main_menu_handler(reply, context: CallbackContext):
    response = f"El apartado de búsqueda le permite encontrar información rápidamente, solo ingrese su consulta.\n\n" \
               f"Podrá encontrar información acerca de lugares, profesores, grupos estudiantiles y demás elementos de la comunidad TEC.\n" \
               f"Para realizar una consulta puede escribir términos como los siguientes:\n\n" \
               f"\U0001f4cd Para encontrar un lugar: \"D3\", \"F2\", \"Pretil\"\n\n" \
               f"\U0001f4d6 Para encontrar una persona: \"secretaria quimica\", \"Juan\""

    reply.text(response)


SEARCH_HANDLERS = HandlerConfig([
    CallbackQueryHandler(one_type_results_paginator, one_type_results_paginator_handler),
    CallbackQueryHandler(page_ty_result, page_ty_result_handler),
    MessageHandler(Filters.text &
                   ~Filters.command &
                   ~Filters.update.edited_message &
                   ~Filters.update.edited_channel_post, search_handler)
])