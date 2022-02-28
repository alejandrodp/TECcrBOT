import html

from telegram.ext import CallbackContext

from tcrb.apps.search.queries import search_query, clean_query
from tcrb.core.apps.handlers.base import Reply
from tcrb.core.apps.pages import show_page


def search_handler(reply: Reply, context: CallbackContext) -> None:
    query = clean_query(reply.text_query())

    def reply_results(results):
        match results:
            case [(ty, [page])]:
                show_page(ty, page['id'], reply)
            case _:
                reply.text(
                    f'No se encontraron resultados para `{html.escape(query)}`')

    return search_query(query, reply_results, reply)
