from django.conf import settings
import importlib

APP_CONFIGS = {app: importlib.import_module(
    '.settings', app) for app in settings.BOT_APPS}
