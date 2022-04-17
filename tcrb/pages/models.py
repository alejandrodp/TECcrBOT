from django.db.models import Model, IntegerField, DateField, TextField


class Page(Model):
    """Representa una página con información, aquí se almacenan todos los identificadores de esas páginas.

    Por ejemplo:
        - Departamentos
        - Personas
        - Servicios
        - Entre otros...

    ty:
    Tipo de página

    title:
    Título de la página

    mtime:
    Fecha de última modificación
    """

    ty = IntegerField()
    title = TextField(max_length=512)
    mtime = DateField(null=True)
