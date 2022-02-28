from whoosh.searching import TimeLimit

from tcrb.apps.search.index import read_index, search
from tcrb.apps.tracking.models import Queries


def query_track_handler(reply, context):
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
