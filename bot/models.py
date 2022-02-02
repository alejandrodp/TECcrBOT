from django.db.models import Model, IntegerField, UniqueConstraint


class Page(Model):
    """Representa una página con información, aquí se almacenan todos los identificadores de esas páginas.

    Por ejemplo:
        - Departamentos
        - Personas
        - Servicios
        - Entre otros...

    ty:
    Tipo de página al que pertenece este identificador.
    """

    ty = IntegerField()
