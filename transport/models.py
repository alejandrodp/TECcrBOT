from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Model, TextField, ForeignKey, DO_NOTHING, IntegerField, TimeField, UniqueConstraint


class TravelType(Model):
    name = TextField(max_length=100)


class Travel(Model):
    start = TextField(max_length=100)
    end = TextField(max_length=100)
    price = IntegerField()
    type = ForeignKey(TravelType, DO_NOTHING)


class TravelStartPoint(Model):
    description = TextField(max_length=1000)
    travel = ForeignKey(Travel, DO_NOTHING)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['description', 'travel'],
                name='travelstartpoint_description_travel_key'
            )
        ]


class ScheduleDay(Model):
    day_index = IntegerField(
        unique=True,
        validators=[
            MaxValueValidator(7),
            MinValueValidator(1)
        ]
    )


class Schedule(Model):
    day = ForeignKey(ScheduleDay, DO_NOTHING)
    time = TimeField()
    start_point = ForeignKey(TravelStartPoint, DO_NOTHING)
    travel = ForeignKey(Travel, DO_NOTHING)
