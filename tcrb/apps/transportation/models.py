from django.db.models import Model, TextField, ForeignKey, DO_NOTHING, IntegerField, TimeField, UniqueConstraint


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

    name = TextField(max_length=100, unique=True)


class Vehicle(Model):
    """Representa el vehículo que se usa para alguna ruta.

    Ejemplo: "Tren", "Bus", etc.

    name:
    Nombre del vehículo.
    """

    name = TextField(max_length=100, unique=True)


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

    source = ForeignKey(Place, DO_NOTHING, related_name="source")
    destination = ForeignKey(Place, DO_NOTHING, related_name="destination")
    vehicle = ForeignKey(Vehicle, DO_NOTHING)
    price = IntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["source", "destination", "vehicle", "price"],
                name="unique_route_key"
            )
        ]


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

    address = TextField(max_length=1000, unique=True)


class Departure(Model):
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
    time = TimeField()
    start = IntegerField()
    end = IntegerField()
    stop = ForeignKey(Stop, DO_NOTHING)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["route", "time", "start", "end"],
                name="consistent_departure_hours_key"
            )
        ]


class BusStop(Model):
    route = ForeignKey(Route, DO_NOTHING)
    stop = ForeignKey(Stop, DO_NOTHING)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["route", "stop"],
                name="unique_stop_route_key"
            )
        ]