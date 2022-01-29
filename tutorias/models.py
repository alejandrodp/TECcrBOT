from django.db.models import Model, TextField, ForeignKey, DO_NOTHING


class School(Model):
    """Representa la unidad academica a la que pertenece la tutoría.

    Puede ser una escuela o un área académica.

    name:
    Nombre de la unidad académica.
    """

    name = TextField(max_length=500)


class Course(Model):
    """Curso al que pertenece la tutoría.

    code:
    Código del curso.

    name:
    Nombre del curso.

    school:
    Unidad académica a la que pertenece la tutoría.
    """

    code = TextField(max_length=50, unique=True)
    name = TextField(max_length=500)
    school = ForeignKey(School, DO_NOTHING)


class Tutoria(Model):
    """Representa la tutoría.

    tutor:
    Nombre del tutor

    schedule:
    Horario de la tutoría.

    place:
    Lugar en el que se imparte la tutoría.

    contact:
    Información de contacto del tutor. También puede ser un grupo de telegram o whatsapp o incluso un servidor
    de discord, etc.

    course:
    Curso de la tutoría.
    """

    tutor = TextField(max_length=100)
    schedule = TextField(max_length=1000)
    place = TextField(max_length=500)
    contact = TextField(max_length=5000)
    course = ForeignKey(Course, DO_NOTHING)
