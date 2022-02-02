import os.path

from environ import ImproperlyConfigured
from whoosh.analysis import LanguageAnalyzer
from whoosh.fields import SchemaClass, NUMERIC, TEXT, ID
from whoosh.index import open_dir, exists_in, create_in
from whoosh.qparser import QueryParser

from django.conf import settings

from bot.pages import read_page_tys

ANALYZER = LanguageAnalyzer('es')


class Schema(SchemaClass):
    ty = NUMERIC(stored=True)
    id = NUMERIC(stored=True)
    title = TEXT(stored=True, analyzer=ANALYZER)
    name = TEXT(analyzer=ANALYZER)
    surname = TEXT(analyzer=ANALYZER)
    email = ID
    tel = ID


_IX_PATH = os.path.join(settings.BASE_DIR, 'index')

try:
    os.mkdir(_IX_PATH)
except FileExistsError:
    pass

_ix = None


def reset_index():
    global _ix
    _ix = create_in(_IX_PATH, schema=Schema)


def open_index():
    global _ix
    if not _ix:
        if exists_in(_IX_PATH):
            _ix = open_dir(_IX_PATH, schema=Schema)
        else:
            reset_index()


def write_index():
    open_index()
    return _ix.writer()


def read_index():
    open_index()
    return _ix.searcher()


def search(searcher, term):
    return searcher.search(QueryParser('title', schema=_ix.schema).parse(term))


def load_pages():
    for ty, ty_obj in read_page_tys().items():
        for doc in ty_obj.index():
            yield ty, doc
