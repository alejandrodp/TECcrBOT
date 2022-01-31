import importlib
import os.path

from environ import ImproperlyConfigured
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

        generator_name = 'generator'
        ty_name = 'ty'
        desc_name = 'desc'

        module_cfg = importlib.import_module('.settings', app)
        page_settings: dict = getattr(module_cfg, 'PAGE_SETTINGS', None)

        if not page_settings:
            continue

        assert generator_name in page_settings and ty_name in page_settings and desc_name in page_settings, \
            f'Page settings improperly configured. Missing "{generator_name}", "{ty_name}" or "{desc_name}" attributes'

        generator = page_settings[generator_name]
        ty = page_settings[ty_name]

        for doc in generator():
            yield ty, doc
