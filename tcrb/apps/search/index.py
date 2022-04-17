import os.path

from django.conf import settings
from whoosh.analysis import CharsetFilter, LowercaseFilter, StopFilter, \
    StemFilter, RegexTokenizer, StandardAnalyzer, default_pattern
from whoosh.collectors import TimeLimitCollector
from whoosh.fields import SchemaClass, NUMERIC, TEXT, ID, KEYWORD
from whoosh.index import open_dir, exists_in, create_in
from whoosh.qparser import MultifieldParser
from whoosh.sorting import FieldFacet
from whoosh.support.charset import accent_map

from tcrb.apps.pages.models import Page

ACCENT_FILTER, STOP_FILTER = CharsetFilter(accent_map), StopFilter(lang='es')

EXACT_ANALYZER = StandardAnalyzer() | STOP_FILTER | ACCENT_FILTER
HINT_ANALYZER = RegexTokenizer(default_pattern) | LowercaseFilter() | \
    STOP_FILTER | ACCENT_FILTER | StemFilter(lang='es')


class Schema(SchemaClass):
    ty = NUMERIC(stored=True)
    id = NUMERIC(stored=True, unique=True)
    title = TEXT(stored=True, analyzer=HINT_ANALYZER, field_boost=1.5)
    kw = KEYWORD(scorable=True, analyzer=HINT_ANALYZER)
    name = TEXT(analyzer=EXACT_ANALYZER, field_boost=2.0)
    surname = TEXT(analyzer=EXACT_ANALYZER, field_boost=2.5)
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
    collector = TimeLimitCollector(searcher.collector(
        groupedby=_TY_FACET), 20e-3, use_alarm=False)
    parser = MultifieldParser(_SEARCH_KWS, schema=_ix.schema)

    searcher.search_with_collector(parser.parse(query), collector)
    return collector.results()


def search_page(searcher, query, pagenum):
    parser = MultifieldParser(_SEARCH_KWS, schema=_ix.schema)
    return searcher.search_page(parser.parse(query), pagenum, pagelen=10)


def load_pages():
    from tcrb.apps.config.init import all_pages
    for ty, ty_obj in all_pages.page_tys.items():
        index = ty_obj.index or (lambda _: {})
        for obj in ty_obj.model.objects.all():
            yield ty, Page.objects.get(id=obj.id), index(obj)
