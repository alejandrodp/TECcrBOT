from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Model, TextField, ForeignKey, DO_NOTHING, IntegerField, TimeField, UniqueConstraint


class Vehicle(Model):
    """Representa el vehículo que se usa durante el viaje.

    Ejemplo: "Tren", "Bus", etc.
    """

    name = TextField(max_length=100)


class Trip(Model):
    """Representa un viaje.

    start_location y end_location:
    Se refieren a la ubicación geográfica de la parada en la que inicia y termina el
    viaje. No son el nombre de la parada específicamente.
    Ejemplos correctos de start_location o end_location:
        - Cartago
        - San José
        - San Carlos
        - Tec Cartago
        - Tec San Carlos

    Ejemplos de lo que NO son start_location o end_location:
        - Parada de buses del TEC Cartago
        - Costado sur de las Ruinas
        - Frente al palo de mango

    price:
    El precio del viaje.

    Type:
    Referencia al vehículo en el que sucede el viaje. A nivel de la base de datos, es una llave foránea
    a la tabla Vehicle.
    """

    start_location = TextField(max_length=100)
    end_location = TextField(max_length=100)
    price = IntegerField()
    type = ForeignKey(Vehicle, DO_NOTHING)


class TripStartPoint(Model):
    """Representa la parada específica en el que inicia el viaje.

    Por ejemplo:
        - Parada de buses del TEC Cartago
        - Costado sur de las Ruinas
        - Frente al palo de mango
    """

    description = TextField(max_length=1000)
    trip = ForeignKey(Trip, DO_NOTHING)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['description', 'trip'],
                name='tripstartpoint_description_trip_key'
            )
        ]


class Schedule(Model):
    """Representa el horario de todos viajes disponibles.

    Contiene la información de a qué horas y dónde se puede iniciar cada viaje.
    """

    day = IntegerField(
        validators=[
            MaxValueValidator(7),
            MinValueValidator(1)
        ]
    )
    time = TimeField()
    start_point = ForeignKey(TripStartPoint, DO_NOTHING)
    travel = ForeignKey(Trip, DO_NOTHING)
