from telegram.ext import CallbackQueryHandler

from bot.menu import main_menu_entry
from tutorias import apps
from tutorias.handlers import school_search, process_school_selection, process_course_selection, previous_page, \
    next_page

HANDLERS = [
    main_menu_entry('Tutorías \U0001f4d6', school_search),
    CallbackQueryHandler(process_school_selection, pattern=rf'{apps.TutoriasConfig.name}:choosing_school:\d*'),
    CallbackQueryHandler(process_course_selection, pattern=rf'{apps.TutoriasConfig.name}:choosing_course:\d*'),
    CallbackQueryHandler(previous_page, pattern=rf'{apps.TutoriasConfig.name}:previous_courses:\d+:\d+'),
    CallbackQueryHandler(next_page, pattern=rf'{apps.TutoriasConfig.name}:next_courses:\d+:\d+'),

]
