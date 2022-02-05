from django.core.paginator import Paginator
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from bot.menu import HandlerMaster
from tutorias import apps
from tutorias.models import School, Course, Tutoria

handlers = HandlerMaster(apps.TutoriasConfig.name)
IKB = InlineKeyboardButton


def school_search(update: Update, context: CallbackContext) -> None:
    if not School.objects.filter(course__tutoria__isnull=False).exists():
        update.message.reply_text(
            text="Aún no se encuentran disponibles las tutorías",
        )
        return

    update.message.reply_text(
        text='Las siguientes escuelas ofrecen tutorías:',
        reply_markup=InlineKeyboardMarkup.from_column(
            [
                IKB(s.name,
                    callback_data=f'{apps.TutoriasConfig.name}:choosing_school:{s.id}')
                for s in School.objects.all()
            ]
        )
    )


def process_school_selection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    school_id = query.data.split(':')[-1]

    db = Course.objects.filter(school_id=school_id).filter(
        tutoria__isnull=False).order_by('code').all()

    pages = Paginator(db, 5)

    _choose_course(query, pages.get_page(1).object_list,
                   school_id, 1, pages.num_pages)


def process_course_selection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    course_id = query.data.split(':')[-1]

    tutorials = _build_tutorials(course_id)

    query.message.edit_text(
        text=f'Se encontraron {len(tutorials)} tutorías para este curso:'
    )

    for t in tutorials:
        query.message.reply_text(
            text=t
        )


def previous_page(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    data = query.data.split(':')

    current_page_index = int(data[-1])
    school_id = data[-2]

    db = Course.objects.filter(school_id=school_id).filter(
        tutoria__isnull=False).order_by('code').all()
    pages = Paginator(db, 5)

    current_page = pages.get_page(current_page_index)

    if current_page.has_previous():
        _choose_course(
            query,
            pages.get_page(current_page.previous_page_number()).object_list,
            school_id,
            current_page.previous_page_number(),
            pages.num_pages)
    else:
        query.answer('Esta es la primera página')


def next_page(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    data = query.data.split(':')

    current_page_index = int(data[-1])
    school_id = data[-2]

    db = Course.objects.filter(school_id=school_id).filter(
        tutoria__isnull=False).order_by('code').all()
    pages = Paginator(db, 5)

    current_page = pages.get_page(current_page_index)

    if current_page.has_next():
        _choose_course(
            query,
            pages.get_page(current_page.next_page_number()).object_list,
            school_id,
            current_page.next_page_number(),
            pages.num_pages)
    else:
        query.answer('Esta es la última página')


def _build_tutorials(course_id):
    tutorials = []

    for tutorial in Tutoria.objects.filter(course_id=course_id).all():
        tutorials.append(
            'Información para la tutoría del curso: {course}\n\n'
            'Tutor: {tutor}\n\n'
            'Se imparte en: {place}\n\n'
            'Horario:\n{schedule}\n\n'
            'Información de contacto:\n{contact}'.format(
                course=f'{tutorial.course.code} - {tutorial.course.name}',
                tutor=tutorial.tutor,
                place=tutorial.place,
                schedule=tutorial.schedule,
                contact=tutorial.contact
            )
        )

    return tutorials


def _choose_course(query, db, school_id, current_page, total_pages):

    query.message.edit_text(
        text='Se ofrecen tutorías para los siguientes cursos:',
        reply_markup=InlineKeyboardMarkup(
            [
                [IKB(f'{course.code} - {course.name}',
                     callback_data=f'{apps.TutoriasConfig.name}:choosing_course:{course.id}')]
                for course in db
            ] + [[
                IKB(text='Regresar a escuelas',
                    callback_data=f'{apps.TutoriasConfig.name}:school_search'),
            ]] + [[
                IKB(text='◀️',
                    callback_data=f'{apps.TutoriasConfig.name}:previous_courses:{school_id}:{current_page}'),
                IKB(text=f'{current_page}/{total_pages}',
                    callback_data='ferwgr'),
                IKB(text='▶️',
                    callback_data=f'{apps.TutoriasConfig.name}:next_courses:{school_id}:{current_page}'),
            ]]
        )
    )
