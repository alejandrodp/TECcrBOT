from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Model, TextField, ForeignKey, DO_NOTHING, IntegerField, TimeField, UniqueConstraint, BooleanField


class Place(Model):
    """Representa una ubicación geográfica en la que inicia o termina una
    ruta. No representa paradas específicamente.
    Ejemplos correctos de un place:
        - Cartago
        - San José
        - San Carlos
        - TEC Cartago
        - TEC San Carlos

    Ejemplos de lo que NO es un place:
        - Parada de buses del TEC Cartago
        - Costado sur de las Ruinas
        - Frente al palo de mango

    name:
    El nombre del lugar.
    """

    name = TextField(max_length=100)


class Vehicle(Model):
    """Representa el vehículo que se usa para alguna ruta.

    Ejemplo: "Tren", "Bus", etc.

    name:
    Nombre del vehículo.
    """

    name = TextField(max_length=100)


class Route(Model):
    """Representa una ruta.

    source:
    Lugar geográfico en el que inicia la ruta (ver place).

    destination:
    Lugar geográfico en el que termina la ruta (ver place).

    vehicle:
    Vehiculo en el que se realiza el viaje.

    price:
    Costo del viaje para esa ruta.
    """

    source = ForeignKey(Place, DO_NOTHING)
    destination = ForeignKey(Place, DO_NOTHING)
    vehicle = ForeignKey(Vehicle, DO_NOTHING)
    price = IntegerField()


class Stop(Model):
    """Representa la parada específica en la ruta. Puede ser la parada inicial o
    alguna durante el viaje.

    Por ejemplo:
        - Parada de buses del TEC Cartago
        - Costado sur de las Ruinas
        - Frente al palo de mango

    route:
    Ruta a la que corresponde la parada.

    time:
    Hora a la que sucede esa parada.

    address:
    Dirección exacta de la parada.

    terminus:
    Determina si es la parada en la que inicia la ruta.
    """

    route = ForeignKey(Route, DO_NOTHING)
    time = TimeField()
    address = TextField(max_length=1000)
    terminus = BooleanField()


class Schedule(Model):
    """Representa la franja de días en las que alguna ruta está disponibles.

    Contiene la información de qué rango de días está disponible cada ruta. Si la ruta
    está disponible solo un día, entonces start y end tienen el mismo valor.

    route:
    Ruta a la que corresponde el horario.

    start:
    Primer día en el rango horario en el que está disponible la ruta.

    end:
    Último día en el rango horario en el que está disponible la ruta.
    """

    route = ForeignKey(Route, DO_NOTHING)
    start = IntegerField(
        validators=[
            MaxValueValidator(7),
            MinValueValidator(1)
        ]
    )
    stop = IntegerField(
        validators=[
            MaxValueValidator(7),
            MinValueValidator(1)
        ]
    )
