from django.core.management.base import BaseCommand
from bot.index import Schema, reset_index, write_index, load_pages


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        index_all()


def index_all():
    reset_index()
    with write_index() as ix:
        for ty, page in load_pages():
            assert 'id' in page and 'title' in page
            ix.add_document(ty=ty, **page)
