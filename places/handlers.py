from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from places import apps
from places.models import Tag, Place

IKB = InlineKeyboardButton


def menu_entry(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        text="Seleccione una categoría:",
        reply_markup=InlineKeyboardMarkup.from_column(
            [
                IKB(tag.name, callback_data=f"{apps.PlacesConfig.name}:tag_id:{tag.id}")
                for tag in Tag.objects.all()
            ]
        )
    )


def select_place(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    tag_id = query.data.split(':')[-1]

    query.message.edit_text(
        text="Seleccione un lugar:",
        reply_markup=InlineKeyboardMarkup.from_column(
            [
                IKB(place.name, callback_data=f"{apps.PlacesConfig.name}:place_id:{place.id}")
                for place in Place.objects.filter(placetagged__tag_id=tag_id).all()
            ]
        )
    )


def get_place(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    place_id = query.data.split(':')[-1]

    place = Place.objects.get(id=place_id)

    name = place.name
    phones = place.contact
    schedules = place.schedule

    response = '<b>Nombre: {name}</b>\n\n<b>Contacto:</b>\n{phones}\n\n<b>Horario:</b>\n{schedule}'.format(
        name=name,
        phones=phones,
        schedule=schedules
    )

    main_message_id = query.edit_message_text(text=response).message_id

    if place.latitude and place.longitude is None:
        update.callback_query.message.reply_text("Ubicación no disponible", reply_to_message_id=main_message_id)
    else:
        update.callback_query.message.reply_location(latitude=place.latitude,
                                                     longitude=place.longitude,
                                                     reply_to_message_id=main_message_id)

    if place.photo.name == '':
        update.callback_query.message.reply_text("Imagen no disponible", reply_to_message_id=main_message_id)
    else:
        update.callback_query.message.reply_photo(place.photo.open(mode='rb'), reply_to_message_id=main_message_id)
