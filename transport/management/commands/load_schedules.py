from django.core.management.base import BaseCommand
import json

from django.db import IntegrityError

from transport.models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        time = ['08:30', '09:30', '10:30', '11:15', '11:30', '12:00']
        travel_id = 3
        start_point = 3

        for day in range(1, 6):
            for t in time:
                Schedule(
                    day_id=day,
                    start_point_id=start_point,
                    travel_id=travel_id,
                    time=t
                ).save()
