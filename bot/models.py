from django.db.models import Model, BigIntegerField, IntegerField, UniqueConstraint


class Page(Model):
    """Representa una página con información, aquí se almacenan todos los identificadores de esas páginas.

    Por ejemplo:
        - Departamentos
        - Personas
        - Servicios
        - Entre otros...

    id:
    Identificador único de la página entre todos los tipos de página.

    ty:
    Tipo de página al que pertenece este identificador.
    """

    id = BigIntegerField(primary_key=True)
    ty = IntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['id', 'ty'],
                name='page_id_type_unique'
            )
        ]
