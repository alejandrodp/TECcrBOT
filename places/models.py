from django.db.models import Model, TextField, UniqueConstraint, ForeignKey, DO_NOTHING, \
    ImageField, FloatField, CheckConstraint, Q, BigIntegerField, UUIDField, CharField


class Place(Model):
    """Representa un lugar.

    Representa un lugar físico. Por ejemplo, un edificio o un espacio que los estudiantes usan.

    name:
    Nombre del lugar.

    latitude:
    latitud del punto.

    lognitude:
    longitud del punto.

    contact_info:
    Información para contactar el lugar. Por ejemplo un número de teléfono.

    schedule:
    El horario de apertura del lugar.

    photo:
    Fotografía del lugar.
    """

    id = BigIntegerField(primary_key=True)
    name = TextField(unique=True, max_length=500)
    latitude = FloatField(null=True)
    longitude = FloatField(null=True)
    contact = TextField(max_length=1000, null=True)
    schedule = TextField(max_length=1000, null=True)
    photo = ImageField(upload_to="places/", null=True)

    class Meta:
        constraints = [
            CheckConstraint(
                check=(Q(latitude__isnull=False) & Q(longitude__isnull=False)) |
                      (Q(latitude__isnull=True) & Q(longitude__isnull=True)),
                name='place_partial_location_not_allowed'
            )
        ]


class Tag(Model):
    """Etiquetas para lugares.

    Cada lugar puede pertenecer a una o más categorías.

    Ejemplos de categorías:
        - Escuela
        - Biblioteca
        - Parqueo
        - Parada de bus

    name:
    Nombre de la etiqueta.
    """
    name = TextField(max_length=500, unique=True)


class PlaceTagged(Model):
    """Lugares con sus etiquetas específicas.

    A nivel de base de datos, representa una tabla intermedia.
    """
    tag = ForeignKey(Tag, DO_NOTHING)
    place = ForeignKey(Place, DO_NOTHING)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['place', 'tag'],
                name="placetagged_place_tag_key"
            )
        ]


class Editor(Model):
    """Representa un usuario que contribuye con la información que muestra el bot.

    telegram_id:
    El id único de la cuenta de usuario de telegram
    """
    telegram_id = BigIntegerField(unique=True)


class Edition(Model):
    """Representa una sugerencia de edición a un lugar determinado.
    Por ejemplo editar el nombre del lugar o su contacto.

    editor:
    El usuario que realiza la edición.

    unique_id:
    ID que permite identificar esta sugerencia entre todas las demás.

    field_type:
    El tipo de edición, puede ser name, contact, location, schedule, tag o photo.

    place:
    El lugar al que se aplica la edición.

    text:
    El contanido de la edición para su revisión y posterior inserción o descarte.

    """
    editor = ForeignKey(Editor, DO_NOTHING)
    unique_id = UUIDField()
    field_type = CharField(max_length=100)
    place = ForeignKey(Place, DO_NOTHING)
    text = CharField(max_length=5000)


class Addition(Model):
    """Representa una sugerencia de adición de algún lugar.

    editor:
    El usuario que realiza la edición.

    text:
    La información del lugar para su revisión y posterior inserción o descarte.

    photo:
    El id (file_id) único de telegram de la foto para su posterior almacenamiento.

    """
    editor = ForeignKey(Editor, DO_NOTHING)
    text = CharField(max_length=5000)
    photo = CharField(max_length=1000, null=True)
