import importlib

from bot.settings import PAGES_MODULES_MAPPING
from tcrb.settings import BOT_APPS


def load_module_pages() -> list:
    pages = []

    for app, ty in PAGES_MODULES_MAPPING:

        if app in BOT_APPS:
            module_cfg = importlib.import_module('.settings', app)

            index_func = getattr(module_cfg, 'INDEX_GENERATOR', None)

            if index_func:
                pages.append({
                    ty: index_func
                })

    return pages
