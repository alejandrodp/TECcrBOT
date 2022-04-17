from telegram.ext import Filters
from whoosh.searching import TimeLimit
from .models import Queries
from ...core.handlers import HandlerConfig, MessageHandler


def query_track_handler(reply, context):
    from tcrb.pages.index import read_index, search
    query = reply.text_query()
    with read_index() as ix:
        try:
            results = search(ix, query)
            if len(results) == 0:
                good_query = False
            else:
                good_query = True
        except TimeLimit:
            good_query = False

        Queries(
            text=query,
            is_good_query=good_query,
            user=reply.user_id()
        ).save()


TRACKING_HANDLERS = HandlerConfig([
    MessageHandler(Filters.text &
                   ~Filters.update.edited_message,
                   query_track_handler)
], 1)
