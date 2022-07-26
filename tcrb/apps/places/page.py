from django.conf import settings

from .models import Place
from .settings import PLACES_DESC
from ...pages import PageTy


def show_place(place: Place, reply):
    message = reply.text(place.description or '')

    if place.latitude and place.longitude:
        message.reply_location(latitude=place.latitude,
                               longitude=place.longitude,
                               reply_to_message_id=message.message_id)
    else:
        message.reply_text("Ubicación no disponible",
                           reply_to_message_id=message.message_id)
    # TODO: No guardar path de fotos en DB, cambiar a path hardcoded y nombre de foto en DB
    if place.photo:
        message.reply_photo(open(settings.BASE_DIR / 'tcrb' / place.photo, mode='rb'),
                            reply_to_message_id=message.message_id)
    else:
        message.reply_text("Imagen no disponible",
                           reply_to_message_id=message.message_id)


PLACES_PAGE = PageTy(ty=4, model=Place, desc=PLACES_DESC, build=show_place)