from telegram import InlineKeyboardMarkup

from tcrb.apps import config
from tcrb.apps.search.buttons import one_type_results_paginator, page_ty_result
from tcrb.apps.search.queries import build_query


def show_one_type_results(ty, results, query, reply):
    paginator = one_type_results_paginator(1, results, ty)
    desc = config.all_pages.page_tys.get(ty).desc
    text = f"Se encontraron los siguientes resultados en {desc} para {build_query(query)}"
    reply.text(text, reply_markup=paginator.markup)


def show_multiple_results(results, query, reply):
    reply.text(f"Se encontraron los siguientes resultados para {build_query(query)}",
               reply_markup=InlineKeyboardMarkup.from_column([
                   page_ty_result(f"{config.all_pages.page_tys.get(ty).desc} ({len(pages)})", ty)
                   for ty, pages in results
               ]))
