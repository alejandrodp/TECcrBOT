import os.path

from environ import ImproperlyConfigured
from whoosh.analysis import CharsetFilter, StandardAnalyzer
from whoosh.fields import SchemaClass, NUMERIC, TEXT, ID
from whoosh.index import open_dir, exists_in, create_in
from whoosh.qparser import MultifieldParser
from whoosh.support.charset import accent_map

from django.conf import settings

from bot.pages import read_page_tys

NO_ACCENT_ANALYZER = StandardAnalyzer() | CharsetFilter(accent_map)


class Schema(SchemaClass):
    ty = NUMERIC(stored=True)
    id = NUMERIC(stored=True, unique=True)
    title = TEXT(stored=True, lang='es')
    name = TEXT(analyzer=NO_ACCENT_ANALYZER, field_boost=1.5)
    surname = TEXT(analyzer=NO_ACCENT_ANALYZER, field_boost=2.0)
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


def search(searcher, query):
    parser = MultifieldParser(['title', 'surname', 'name'], schema=_ix.schema)
    return searcher.search(parser.parse(query))


def load_pages():
    for ty, ty_obj in read_page_tys().items():
        for doc in ty_obj.index():
            yield ty, doc
