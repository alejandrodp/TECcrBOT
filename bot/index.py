import os.path

from django.conf import settings
from whoosh.analysis import CharsetFilter, StopFilter, LanguageAnalyzer, StandardAnalyzer
from whoosh.collectors import TimeLimitCollector
from whoosh.fields import SchemaClass, NUMERIC, TEXT, ID, KEYWORD
from whoosh.index import open_dir, exists_in, create_in
from whoosh.lang.stopwords import stoplists
from whoosh.qparser import MultifieldParser
from whoosh.sorting import FieldFacet
from whoosh.support.charset import accent_map

from tcrb.core import PageTy
from .models import Page

LANGUAGE_ANALYZER = LanguageAnalyzer('es')
NO_ACCENT_ANALYZER = StandardAnalyzer() | StopFilter(stoplists['es']) | CharsetFilter(accent_map)


class Schema(SchemaClass):
    ty = NUMERIC(stored=True)
    id = NUMERIC(stored=True, unique=True)
    title = TEXT(stored=True, analyzer=LANGUAGE_ANALYZER, field_boost=1.5)
    kw = KEYWORD(scorable=True, analyzer=LANGUAGE_ANALYZER)
    name = TEXT(analyzer=NO_ACCENT_ANALYZER, field_boost=2.0)
    surname = TEXT(analyzer=NO_ACCENT_ANALYZER, field_boost=2.5)
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


_SEARCH_KWS = ['title', 'surname', 'name', 'kw']
_TY_FACET = FieldFacet('ty')


def search(searcher, query):
    collector = TimeLimitCollector(searcher.collector(groupedby=_TY_FACET), 20e-3, use_alarm=False)
    parser = MultifieldParser(_SEARCH_KWS, schema=_ix.schema)

    searcher.search_with_collector(parser.parse(query), collector)
    return collector.results()


def load_pages():
    for ty, ty_obj in PageTy.read_page_tys().items():
        index = ty_obj.index or (lambda _: {})
        for obj in ty_obj.model.objects.all():
            yield ty, Page.objects.get(id=obj.id), index(obj)
