from telegram.ext import Filters, MessageHandler, CallbackQueryHandler

from tutorials.handlers import *

MAIN_MENU_COMMAND = 'Tutorías 📖'


HANDLERS = [

    MessageHandler(Filters.text(MAIN_MENU_COMMAND), main_entry),
    CallbackQueryHandler(school_search, pattern=f'{apps.TutorialsConfig.name}:school_search'),
    CallbackQueryHandler(course_search, pattern=f'{apps.TutorialsConfig.name}:course_search'),
    CallbackQueryHandler(process_school_selection, pattern=rf'{apps.TutorialsConfig.name}:choosing_school:\d*'),
    CallbackQueryHandler(process_course_selection, pattern=rf'{apps.TutorialsConfig.name}:choosing_course:\d*'),


]