from django.db.models import Model, TextField, ForeignKey, DO_NOTHING


class School(Model):
    name = TextField(max_length=500)


class Course(Model):
    code = TextField(max_length=6, unique=True)
    name = TextField(max_length=500)
    school = ForeignKey(School, DO_NOTHING)


class Tutorial(Model):
    tutor = TextField(max_length=100)
    schedule = TextField(max_length=1000)
    place = TextField(max_length=500)
    contact = TextField(max_length=5000)
    course = ForeignKey(Course, DO_NOTHING)
