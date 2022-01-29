from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from tutorias import apps
from tutorias.models import School, Course, Tutoria

IKB = InlineKeyboardButton


def main_entry(update: Update, context: CallbackContext) -> None:
    if not School.objects.filter(course__tutorial__isnull=False).exists():
        update.message.reply_text(
            text="Aún no se encuentran disponibles las tutorías",
        )
        return

    update.message.reply_text(
        text="Seleccione un método de búsqueda:",
        reply_markup=InlineKeyboardMarkup.from_column(
            [
                IKB('Buscar por escuela', callback_data=f'{apps.TutoriasConfig.name}:school_search'),
                IKB('Buscar por curso', callback_data=f'{apps.TutoriasConfig.name}:course_search')
            ]
        )
    )


def school_search(update: Update, context: CallbackContext) -> None:
    update.callback_query.message.edit_text(
        text='Las siguientes escuelas ofrecen tutorías:',
        reply_markup=InlineKeyboardMarkup.from_column(
            [
                IKB(s.name, callback_data=f'{apps.TutoriasConfig.name}:choosing_school:{s.id}')
                for s in School.objects.filter(course__tutorial__isnull=False).all()
            ]
        )
    )


def process_school_selection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    school_id = query.data.split(':')[-1]

    _choose_course(query, school_id)


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


def course_search(update: Update, context: CallbackContext) -> None:
    _choose_course(update.callback_query)


def _choose_course(query, school_id=None):
    if school_id:
        db = Course.objects.filter(school_id=school_id)
    else:
        db = Course.objects

    query.message.edit_text(
        text='Se ofrecen tutorías para los siguientes cursos:',
        reply_markup=InlineKeyboardMarkup.from_column(
            [
                IKB(f'{course.code} - {course.name}', callback_data=f'{apps.TutoriasConfig.name}:choosing_course:{course.id}')
                for course in db.filter(tutorial__isnull=False).all()
            ]
        )
    )
