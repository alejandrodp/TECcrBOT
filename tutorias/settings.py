from bot.menu import main_menu_entry
from tutorias.handlers import school_search, process_school_selection, process_course_selection, previous_page, \
    next_page, handlers

main_menu_entry('Tutorías \U0001f4d6', school_search)
handlers.add_callback_query_handler(process_school_selection, 'choosing_school', r'\d+')
handlers.add_callback_query_handler(process_course_selection, 'choosing_course', r'\d+')
handlers.add_callback_query_handler(previous_page, 'previous_courses', r'\d+', r'\d+')
handlers.add_callback_query_handler(next_page, 'next_courses', r'\d+', r'\d+')
