from django.db.models import Model, CharField, DateTimeField, BooleanField, BigIntegerField
from django.utils import timezone


class Queries(Model):
    text = CharField(max_length=5000)
    ctime = DateTimeField(default=timezone.now)
    is_good_query = BooleanField(null=True)
    user = BigIntegerField(null=True)
