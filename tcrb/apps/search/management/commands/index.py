from django.core.management.base import BaseCommand
from tcrb.pages.index import reset_index, write_index, load_pages


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        index_all()


def index_all():
    reset_index()
    with write_index() as ix:
        for ty, page, doc in load_pages():
            assert not any(key in doc for key in ('ty', 'id', 'title'))
            ix.add_document(ty=ty, id=page.id, title=page.title, **doc)
