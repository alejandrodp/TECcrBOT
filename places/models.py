from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Model, DecimalField, TextField, UniqueConstraint, ForeignKey, DO_NOTHING, \
    CharField, IntegerField, TimeField, ImageField


class Location(Model):
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
    name = TextField(unique=True, max_length=500)
    location = ForeignKey(Location, DO_NOTHING, null=True)
    photo = ImageField(upload_to="places/", null=True)


# class PlaceSynonym(Model):
#     name = TextField(max_length=500)
#     place = ForeignKey(Place, DO_NOTHING)
#
#     class Meta:
#         constraints = [
#             UniqueConstraint(
#                 fields=['name', 'place'],
#                 name="synonym_name_place_key"
#             )
#         ]


class Phone(Model):
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


class ScheduleDay(Model):
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
    day = ForeignKey(ScheduleDay, DO_NOTHING)
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
    name = TextField(max_length=500, unique=True)


# class TagSynonym(Model):
#     name = TextField(max_length=500, unique=True)
#     tag = ForeignKey(Tag, DO_NOTHING)


class PlaceTagged(Model):
    tag = ForeignKey(Tag, DO_NOTHING)
    place = ForeignKey(Place, DO_NOTHING)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['place', 'tag'],
                name="placetagged_place_tag_key"
            )
        ]
