import importlib

from bot.settings import PAGES_MODULES_MAPPING
from tcrb.settings import BOT_APPS


def load_module_pages():
    for app, ty in PAGES_MODULES_MAPPING.items():
        if app not in BOT_APPS:
            continue 

        module_cfg = importlib.import_module('.settings', app)
        index_func = getattr(module_cfg, 'INDEX_GENERATOR', None)

        if index_func:
            for doc in index_func():
                yield (ty, doc)
