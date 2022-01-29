import json
import logging

from django.core.management.base import BaseCommand

from bot.initial import start_polling

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        tags = json.load(open('/home/alejandro/projects/tcrb/tags2.json'))

        for k, v in tags.items():

            name = k.split(' - ')[-1]






