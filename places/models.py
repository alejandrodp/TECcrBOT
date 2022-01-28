from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Model, DecimalField, TextField, UniqueConstraint, ForeignKey, DO_NOTHING, \
    CharField, IntegerField, TimeField, ImageField


class Location(Model):
    """Representa un punto geográfico.

    Utiliza coordenadas para representar el punto.

    latitude:
    latitud del punto.

    lognitude:
    longitud del punto.
    """

    latitude = DecimalField(max_digits=10, decimal_places=6)
    longitude = DecimalField(max_digits=10, decimal_places=6)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['latitude', 'longitude'],
                name="location_latitude_longitude_key"
            )
        ]


class Place(Model):
    """Representa un lugar.

    Representa un lugar físico. Por ejemplo, un edificio o un espacio que los estudiantes usan.

    name:
    Nombre del lugar.

    location:
    Punto geográfico en el que está el lugar.

    photo:
    Fotografía del lugar.
    """

    name = TextField(unique=True, max_length=500)
    location = ForeignKey(Location, DO_NOTHING, null=True)
    photo = ImageField(upload_to="places/", null=True)


class Phone(Model):
    """Número de telefono.

    Números de telefono con una breve descripción.
    """

    place = ForeignKey(Place, DO_NOTHING)
    phone = CharField(max_length=8)
    details = TextField(null=True, max_length=1000)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['place', 'phone'],
                name="phone_place_phone_key"
            )
        ]


class WeekDay(Model):
    """Días de la semana.

    Lunes, Martes, Miércoles, Jueves, Viernes, Sábado, Domingo

    place:
    Lugar correspondiente al día.
    """

    place = ForeignKey(Place, DO_NOTHING)
    day_index = IntegerField(
        validators=[
            MaxValueValidator(7),
            MinValueValidator(1)
        ]
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['place', 'day_index'],
                name="scheduleday_place_day_index_key"
            )
        ]


class ScheduleTime(Model):
    """Representa el horario de algún lugar.

    Día y horas en los que algún lugar está abierto al público.

    day:
    Día de la semana en el que lugar está abierto.

    start:
    Hora a la que abre el lugar.

    end:
    Hora a la que cierra el lugar.

    details:
    Breve descripción o comentario.
    """

    day = ForeignKey(WeekDay, DO_NOTHING)
    start = TimeField()
    end = TimeField()
    details = TextField(null=True, max_length=1000)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['day', 'start', 'end'],
                name="schedule_time_day_start_end_key"
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
