from typing import List, Optional

from django.conf import settings
from telegram import InlineKeyboardButton, Update

from common.util import send_text
from .models import Place


def index_places():
    for place in Place.objects.all():
        yield {
            'id': place.id,
            'title': place.name,
        }


def show_place(page: int, update: Update) -> (str, Optional[List[InlineKeyboardButton]]):

    if not Place.objects.filter(id=page).exists():
        send_text("Página no encontrada", update)
        return

    place = Place.objects.get(id=page)

    desc = place.description if place.description else "No disponible"

    text = f"<b>Nombre: {place.name}</b>\n\n" \
          f"Descripción:\n" \
          f"{desc}"

    message = send_text(text, update)

    if place.latitude and place.longitude:
        message.reply_location(latitude=place.latitude,
                               longitude=place.longitude,
                               reply_to_message_id=message.message_id)
    else:
        message.reply_text("Ubicación no disponible", reply_to_message_id=message.message_id)

    if place.photo:
        message.reply_photo(open(settings.BASE_DIR / place.photo, mode='rb'),
                            reply_to_message_id=message.message_id)
    else:
        message.reply_text("Imagen no disponible", reply_to_message_id=message.message_id)


