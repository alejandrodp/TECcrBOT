from telegram.ext import Filters, MessageHandler, CallbackQueryHandler

from tutorias import apps
from tutorias.handlers import school_search, process_school_selection, process_course_selection, previous_page,\
    next_page

MAIN_MENU_COMMAND = 'Tutorías 📖'


HANDLERS = [

    MessageHandler(Filters.text(MAIN_MENU_COMMAND), school_search),
    CallbackQueryHandler(process_school_selection, pattern=rf'{apps.TutoriasConfig.name}:choosing_school:\d*'),
    CallbackQueryHandler(process_course_selection, pattern=rf'{apps.TutoriasConfig.name}:choosing_course:\d*'),
    CallbackQueryHandler(previous_page, pattern=rf'{apps.TutoriasConfig.name}:previous_courses:\d+:\d+'),
    CallbackQueryHandler(next_page, pattern=rf'{apps.TutoriasConfig.name}:next_courses:\d+:\d+'),


]