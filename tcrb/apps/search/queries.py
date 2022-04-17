import html
import re

from whoosh.searching import TimeLimit

QUERY_DELIMITER = "`"


def search_query(query: str, callback, reply):
    from tcrb.apps.search import index

    with index.read_index() as ix:
        try:
            results = index.search(ix, query)
        except TimeLimit:
            reply.fail(
                f"Su búsqueda ha tardado demasiado, intente una más simple")

        docnums = {hit.docnum: hit for hit in results}
        hits = ((ty, [docnums.pop(no) for no in hits])
                for ty, hits in results.groups().items())

        groups = sorted(hits, key=lambda e: e[1][0].score, reverse=True)
        return callback(groups)


def clean_query(query: str):
    return query.replace(QUERY_DELIMITER, "")


def get_query(text: str):
    try:
        query = re.search(rf'{QUERY_DELIMITER}(.+?){QUERY_DELIMITER}', text).group(1)
    except AttributeError:
        raise AttributeError("Query not found.")
    else:
        return query


def build_query(text):
    return f"{QUERY_DELIMITER}{html.escape(text)}{QUERY_DELIMITER}"
