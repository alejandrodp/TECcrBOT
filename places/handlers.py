import base64
import binascii
import json
from json import JSONDecodeError
from uuid import uuid4, UUID

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

from bot.menu import BotHandler
from places import apps
from places.constants import CONTRIBUTION_TYPE
from places.models import Tag, Place, Editor, Edition

handlers = BotHandler(apps.PlacesConfig.name)

def menu_entry(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        text="Seleccione una categoría:",
        reply_markup=InlineKeyboardMarkup.from_column(
            [
                handlers.build_inline_button(tag.name, 'tag_id', tag.id)
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
                IKB(place.name,
                    callback_data=f"{apps.PlacesConfig.name}:place_id:{place.id}")
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

    main_message_id = query.edit_message_text(
        text=response,
        reply_markup=InlineKeyboardMarkup.from_column([
            IKB('Sugerir cambio',
                callback_data=f'{apps.PlacesConfig.name}:select_edit:{place_id}'),
        ])
    ).message_id

    if place.latitude and place.longitude is None:
        update.callback_query.message.reply_text(
            "Ubicación no disponible", reply_to_message_id=main_message_id)
    else:
        update.callback_query.message.reply_location(latitude=place.latitude,
                                                     longitude=place.longitude,
                                                     reply_to_message_id=main_message_id)

    if place.photo.name == '':
        update.callback_query.message.reply_text(
            "Imagen no disponible", reply_to_message_id=main_message_id)
    else:
        update.callback_query.message.reply_photo(
            place.photo.open(mode='rb'), reply_to_message_id=main_message_id)


def select_edit(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data.split(':')
    query.answer()

    place_id = data[-1]

    query.message.reply_text(
        text='Seleccione el tipo de sugerencia:',
        reply_to_message_id=query.message.message_id,
        reply_markup=InlineKeyboardMarkup.from_column([
            IKB('Nombre',
                callback_data=f'{apps.PlacesConfig.name}:request_edit:0:{place_id}'),
            IKB('Ubicación',
                callback_data=f'{apps.PlacesConfig.name}:request_edit:1:{place_id}'),
            IKB('Información de contacto',
                callback_data=f'{apps.PlacesConfig.name}:request_edit:2:{place_id}'),
            IKB('Horario de apertura',
                callback_data=f'{apps.PlacesConfig.name}:request_edit:3:{place_id}'),
            IKB('Imagen',
                callback_data=f'{apps.PlacesConfig.name}:request_edit:4:{place_id}'),
        ])
    )


def request_edit(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data.split(':')

    place_id = data[-1]
    edit_type = int(data[-2])
    place_name = Place.objects.get(id=place_id).name

    data = {
        'ty': edit_type,
        't': uuid4().hex,
        'i': int(place_id)
    }

    data_encoded = base64.b64encode(
        json.dumps(data).encode('ascii')).decode('ascii')

    title = CONTRIBUTION_TYPE[edit_type]['message']
    foot = CONTRIBUTION_TYPE[edit_type]['foot']

    query.message.edit_text(
        text=f'{title} <i>{place_name}</i>\n'
             f'Ticket: {data["t"]}\n'
             f'Datos: {data_encoded}\n\n'
             f'<b>{foot}\n'
             f'Si incluye fuentes confiables será más probable que su contribución sea aceptada.</b>',
    )


def _process_edition(ty, ticket, i, editor, update: Update) -> None:
    text = '{data_type}:\n{object_data}\n\nDetalles:\n{details}'.format(
        data_type=CONTRIBUTION_TYPE[ty]['db_name'],
        object_data='{object_data}',
        details='{details}'

    )
    location = update.message.location

    if ty == 1 and location:
        text = text.format(
            object_data='\n'.join(
                [f'Latitud: {location.latitude}', f'Longitud: {location.longitude}']),
            details='Sin detalles'
        )
    elif ty == 4 and update.message.photo:
        text = text.format(
            object_data=','.join([
                p.file_id
                for p in update.message.photo
            ]),
            details=update.message.caption if update.message.caption else 'Sin detalles'
        )
    else:
        text = text.format(
            object_data=update.message.text,
            details='Sin detalles'
        )

    Edition(
        unique_id=ticket,
        field_type=CONTRIBUTION_TYPE[ty]['db_name'],
        text=text,
        editor=editor,
        place_id=i
    ).save()


def handle_text_edit(update: Update, context: CallbackContext) -> None:
    data = context.match.groups()[0]
    user_id = update.effective_user.id

    try:
        decoded_data = json.loads(base64.b64decode(data, validate=True))

        ty = int(decoded_data['ty'])
        ticket = UUID(decoded_data['t'])
        i = int(decoded_data['i'])

        if not Editor.objects.filter(telegram_id=user_id).exists():
            editor = Editor(telegram_id=user_id)
            editor.save()
        else:
            editor = Editor.objects.get(telegram_id=user_id)

        if not Edition.objects.filter(unique_id=ticket).exists():
            _process_edition(ty, ticket, i, editor, update)

            update.message.reply_text(
                text='Gracias por su contribución, se le notificará en caso de ser aceptada por los moderadores.'
            )
        else:
            update.message.reply_text(
                text='Ya se realizó la contribución, '
                     'para generar una nueva contribución por favor use el menú bajo el mensaje del lugar.'
            )

    except (binascii.Error, JSONDecodeError, UnicodeDecodeError, ValueError, KeyError) as e:
        update.message.reply_text(
            'Hubo un problema procesando su solicitud. Intente de nuevo.')
        raise e
