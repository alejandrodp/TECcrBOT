import importlib
import os.path

from whoosh.analysis import LanguageAnalyzer
from whoosh.fields import SchemaClass, NUMERIC, TEXT
from whoosh.index import open_dir, exists_in, create_in
from whoosh.qparser import QueryParser

from django.conf import settings

ANALYZER = LanguageAnalyzer('es')


class Schema(SchemaClass):
    ty = NUMERIC(stored=True)
    id = NUMERIC(stored=True)
    title = TEXT(stored=True, analyzer=ANALYZER)
    author = TEXT(analyzer=ANALYZER)


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
    for app in settings.BOT_APPS:

        module_cfg = importlib.import_module('.settings', app)
        index_func = getattr(module_cfg, 'INDEX_GENERATOR', None)
        ty = getattr(module_cfg, 'PAGE_TY', None)

        if index_func and ty:
            for doc in index_func():
                yield ty, doc
