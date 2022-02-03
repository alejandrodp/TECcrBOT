from django.conf import settings
import importlib

MAIN_MENU = [
    ['Búsqueda \U0001f50d', 'Servicios de transporte 🚌'],
    ['Ubicaciones 📍', 'Tutorías 📖'],
    ['Noticias TEC 📰', 'Info 🤖']]

APP_CONFIGS = {app: importlib.import_module('.settings', app) for app in settings.BOT_APPS}
