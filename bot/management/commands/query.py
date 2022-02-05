import sys

from django.core.management.base import BaseCommand
from whoosh.collectors import TimeLimit

from bot.index import read_index, search
from bot.pages import read_page_tys
from tcrb.core import PageTy


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('query')

    def handle(self, *args, **kwargs):
        page_tys = read_page_tys()
        with read_index() as ix:
            try:
                results = search(ix, kwargs['query'])
            except TimeLimit:
                print('Error: query timed out', file=sys.stderr)
                return

            print(results, file=sys.stderr)

            docnums = {hit.docnum: hit for hit in results}
            hits = ((ty, [docnums.pop(no) for no in hits])
                    for ty, hits in results.groups().items())

            groups = sorted(hits, key=lambda e: e[1][0].score, reverse=True)
            for ty, ty_hits in groups:
                desc = page_tys[ty].desc
                print(f'\n{desc} ({len(ty_hits)}):')

                for hit in ty_hits:
                    print(hit)
