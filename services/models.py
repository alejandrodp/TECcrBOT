from django.db.models import Model, TextField, URLField, BigIntegerField, CharField


class Service(Model):
    """Representa un algún servicio que la institución brinda.

    Por ejemplo:
        - Psicología
        - Clínica
        - Impresión en 3D
        - Fotocipiado

    name:
    Nombre del servicio.

    description:
    Breve descripción del servicio.

    link:
    Url del servicio en la página del Tec.

    contact:
    Información de contacto para usar el servicio.
    """

    id = BigIntegerField(primary_key=True)
    name = CharField(max_length=500, unique=True)
    description = TextField(max_length=5000, null=True)
    link = URLField(max_length=500, null=True)
    contact = CharField(max_length=5000, null=True)
