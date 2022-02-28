from django.db.models import \
    Model, BooleanField, TextField, ForeignKey, DO_NOTHING


class Person(Model):
    """Representa una persona en el directorio del bot.

    name:
    Nombre de la persona.

    surname:
    Apellidos de la persona.

    email:
    Correo de la persona.

    phone:
    Número de la persona.

    href:
    Url al perfil de la persona en la página del tec.
    """

    name = TextField(max_length=100)
    surname = TextField(max_length=100)
    email = TextField(max_length=500, null=True)
    phone = TextField(max_length=100, null=True)
    href = TextField(max_length=1000)


class Ty(Model):
    """Se refiere al "tipo" o "puesto" que tiene una persona dentro de un departamento.

    Por ejemplo, "coordinador", "directora", "presidente" etc.

    name:
    Nombre del tipo.
    """

    name = TextField(max_length=100, unique=True)


class Location(Model):
    """Ubicaciones de las diferentes unidades.

    Por lo general, sirve para diferenciar unidades que son iguales pero están en diferentes campus.
    Por ejemplo, para diferenciar entre la Escuela de Matemática de Cartago y la de San José.

    name:
    Nombre del departamento.
    """

    name = TextField(max_length=100, unique=True)
    href = TextField(max_length=1000)


class Unit(Model):
    """Departamentos, unidades, escuelas, etc.

    name:
    Nombre de la unidad.
    """

    name = TextField(max_length=100, unique=True)
    href = TextField(max_length=1000)


class Role(Model):
    """Rol que cumple la persona en su respectivo departamento.

    Está compuesto por su tipo y su función. Ver documentación de tipo y función.

    person:
    Persona que ejerce el rol.

    department:
    Departamento en el cual la persona ejerce el rol.

    type:
    Tipo de rol.

    function:
    Función del rol.
    """

    person = ForeignKey(Person, DO_NOTHING)
    unit = ForeignKey(Unit, DO_NOTHING)
    location = ForeignKey(Location, DO_NOTHING, null=True)


class RoleTy(Model):
    role = ForeignKey(Role, DO_NOTHING)
    ty = ForeignKey(Ty, DO_NOTHING)
    is_function = BooleanField()
