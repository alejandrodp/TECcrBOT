from telegram.ext import Filters, MessageHandler, CallbackQueryHandler

from tutorias.handlers import *

MAIN_MENU_COMMAND = 'Tutorías 📖'


HANDLERS = [

    MessageHandler(Filters.text(MAIN_MENU_COMMAND), main_entry),
    CallbackQueryHandler(school_search, pattern=f'{apps.TutoriasConfig.name}:school_search'),
    CallbackQueryHandler(course_search, pattern=f'{apps.TutoriasConfig.name}:course_search'),
    CallbackQueryHandler(process_school_selection, pattern=rf'{apps.TutoriasConfig.name}:choosing_school:\d*'),
    CallbackQueryHandler(process_course_selection, pattern=rf'{apps.TutoriasConfig.name}:choosing_course:\d*'),


]