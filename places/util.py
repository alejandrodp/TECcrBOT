from typing import List, Optional

from telegram import Message, InlineKeyboardButton

from .models import Place


def index_places():
    for place in Place.objects.all():
        yield {
            'id': place.id,
            'title': place.name,
        }


def show_place(page: int) -> (str, Optional[List[InlineKeyboardButton]]):
    place = Place.objects.get(id=page)
    return f'Nombre: {place.name}', None
