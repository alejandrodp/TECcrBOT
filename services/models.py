from django.db.models import Model, TextField, URLField


class Service(Model):
    name = TextField(max_length=500, unique=True)
    description = TextField(max_length=5000)
    link = URLField(max_length=500)
    contact = TextField(max_length=5000)



