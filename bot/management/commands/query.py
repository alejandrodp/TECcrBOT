from django.core.management.base import BaseCommand
from bot.index import read_index, search


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('query')

    def handle(self, *args, **kwargs):
        with read_index() as ix:
            results = search(ix, kwargs['query'])
            print(results)
            for hit in results:
                print(hit)
