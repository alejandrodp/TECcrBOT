from django.db.models import Model, FloatField, CheckConstraint, Q, BigIntegerField, CharField


class Place(Model):
    """Representa un lugar.

    Representa un lugar físico. Por ejemplo, un edificio o un espacio que los estudiantes usan.

    name:
    Nombre del lugar.

    latitude:
    latitud del punto.

    lognitude:
    longitud del punto.

    description:
    Descripción del lugar

    photo:
    Fotografía del lugar.
    """

    id = BigIntegerField(primary_key=True)
    name = CharField(unique=True, max_length=500)
    latitude = FloatField(null=True)
    longitude = FloatField(null=True)
    description = CharField(max_length=5000, null=True)
    photo = CharField(max_length=1000, null=True)

    class Meta:
        constraints = [
            CheckConstraint(
                check=(Q(latitude__isnull=False) & Q(longitude__isnull=False)) |
                (Q(latitude__isnull=True) & Q(longitude__isnull=True)),
                name='place_partial_location_not_allowed'
            )
        ]
