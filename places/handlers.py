from django.db.models import QuerySet
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from places import apps
from common.constants import DAYS_MAPPING
from places.models import Tag, Place, Phone, ScheduleDay

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
    phones = _get_phones(place.phone_set)
    schedules = _get_schedule(place.scheduleday_set)
    location = place.location

    response = "<b>Nombre: {name}</b>\n\n<b>Teléfonos:</b>\n{phones}\n\n<b>Horario:</b>\n{schedule}".format(
        name=name,
        phones=phones,
        schedule=schedules
    )

    main_message_id = query.edit_message_text(text=response).message_id

    if location is None:
        update.callback_query.message.reply_text("Ubicación no disponible", reply_to_message_id=main_message_id)
    else:
        update.callback_query.message.reply_location(latitude=float(location.latitude),
                                                     longitude=float(location.longitude),
                                                     reply_to_message_id=main_message_id)

    if place.photo.name == '':
        update.callback_query.message.reply_text("Imagen no disponible", reply_to_message_id=main_message_id)
    else:
        update.callback_query.message.reply_photo(place.photo.open(mode='rb'), reply_to_message_id=main_message_id)


def _get_phones(phones_set: QuerySet[Phone]) -> str:
    if not phones_set.exists():
        return "No disponible"

    phones = []

    for p in phones_set.all():
        phones.append(
            "{phone}{details}".format(
                phone=p.phone,
                details=f" ({p.details})" if p.details is not None and p.details != '' else ''
            )
        )

    return "\n".join(phones)


def _get_schedule(days: QuerySet[ScheduleDay]) -> str:
    if not days.exists():
        return "No disponible"

    schedules = []

    for day in days.order_by('day_index').all():
        time = '\n'.join(
            ["{start} - {end}{details}".format(
                start=time.start,
                end=time.end,
                details=f" ({time.details})" if time.details is not None and time.details != '' else '')
                for time in day.scheduletime_set.order_by('start').all()]
        ) if day.scheduletime_set.exists() else "Cerrado"

        schedules.append(
            "<i>{day}:</i>\n{time}".format(
                day=DAYS_MAPPING.get(day.day_index),
                time=time
            )
        )

    return "\n\n".join(schedules)
