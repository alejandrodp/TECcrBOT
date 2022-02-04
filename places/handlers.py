from enum import Enum

from django.core.paginator import Paginator
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from bot.menu import BotHandler
from common.util import is_int, send_unknown_error
from places import apps
from places.models import Tag, Place

handlers = BotHandler(apps.PlacesConfig.name)


class States(Enum):
    SELECT_CATEGORY = "select_location_category"
    GET_CATEGORY = "get_category"


def menu_entry(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        text="En esta sección puede ver todas las ubicaciones disponibles por categorías.\n"
             "También puede buscar una ubicación escribiendo el nombre (Ejemplos: A1, fotocopiadora)",
        reply_markup=InlineKeyboardMarkup.from_column(
            [
                handlers.build_inline_button("Ver categorías", States.SELECT_CATEGORY)
            ]
        )
    )


def first_category_list(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    send_category_list(1, query)


def remain_category_list(update: Update, context: CallbackContext) -> None:
    current_page = context.match.group(1)
    query = update.callback_query
    query.answer()

    if is_int(current_page):
        current_page = int(current_page)
    else:
        send_unknown_error(update.effective_chat)

    send_category_list(current_page, query)


def send_category_list(current_page_num, query):
    pages = Paginator(Tag.objects.order_by('name').all(), 5)

    current_pages = pages.get_page(current_page_num)

    buttons = [handlers.build_inline_button(tag.name, States.GET_CATEGORY, str(tag.id))
               for tag in current_pages.object_list]

    paginator = handlers.build_paginator(
        current_page_num,
        States.SELECT_CATEGORY,
        pages,
        buttons
    )

    query.edit_message_text(
        text="Seleccione una categoría:",
        reply_markup=paginator.markup
    )


def select_place(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    tag_id = query.data.split(':')[-1]

    query.message.edit_text(
        text="Seleccione un lugar:",
        reply_markup=InlineKeyboardMarkup.from_column(
            [
                handlers.build_inline_button(place.name, 'place_id', str(place.id))
                for place in Place.objects.filter(placetagged__tag_id=int(tag_id)).all()
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
            handlers.build_inline_button('Sugerir cambio', 'select_edit', str(place_id))
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

# def select_edit(update: Update, context: CallbackContext) -> None:
#     query = update.callback_query
#     data = query.data.split(':')
#     query.answer()
#
#     place_id = data[-1]
#
#     query.message.reply_text(
#         text='Seleccione el tipo de sugerencia:',
#         reply_to_message_id=query.message.message_id,
#         reply_markup=InlineKeyboardMarkup.from_column([
#             handlers.build_inline_button('Nombre', 'request_edit', '0', str(place_id)),
#             handlers.build_inline_button('Ubicación', 'request_edit', '1', str(place_id)),
#             handlers.build_inline_button('Información de contacto', 'request_edit', '2', str(place_id)),
#             handlers.build_inline_button('Horario de apertura', 'request_edit', '2', str(place_id)),
#             handlers.build_inline_button('Imagen', 'request_edit', '4', str(place_id)),
#         ])
#     )
#
#
# def request_edit(update: Update, context: CallbackContext) -> None:
#     query = update.callback_query
#     data = query.data.split(':')
#
#     place_id = data[-1]
#     edit_type = int(data[-2])
#     place_name = Place.objects.get(id=place_id).name
#
#     data = {
#         'ty': edit_type,
#         't': uuid4().hex,
#         'i': int(place_id)
#     }
#
#     data_encoded = base64.b64encode(
#         json.dumps(data).encode('ascii')).decode('ascii')
#
#     title = CONTRIBUTION_TYPE[edit_type]['message']
#     foot = CONTRIBUTION_TYPE[edit_type]['foot']
#
#     query.message.edit_text(
#         text=f'{title} <i>{place_name}</i>\n'
#              f'Ticket: {data["t"]}\n'
#              f'Datos: {data_encoded}\n\n'
#              f'<b>{foot}\n'
#              f'Si incluye fuentes confiables será más probable que su contribución sea aceptada.</b>',
#     )
#
#
# def _process_edition(ty, ticket, i, editor, update: Update) -> None:
#     text = '{data_type}:\n{object_data}\n\nDetalles:\n{details}'.format(
#         data_type=CONTRIBUTION_TYPE[ty]['db_name'],
#         object_data='{object_data}',
#         details='{details}'
#
#     )
#     location = update.message.location
#
#     if ty == 1 and location:
#         text = text.format(
#             object_data='\n'.join(
#                 [f'Latitud: {location.latitude}', f'Longitud: {location.longitude}']),
#             details='Sin detalles'
#         )
#     elif ty == 4 and update.message.photo:
#         text = text.format(
#             object_data=','.join([
#                 p.file_id
#                 for p in update.message.photo
#             ]),
#             details=update.message.caption if update.message.caption else 'Sin detalles'
#         )
#     else:
#         text = text.format(
#             object_data=update.message.text,
#             details='Sin detalles'
#         )
#
#     Edition(
#         unique_id=ticket,
#         field_type=CONTRIBUTION_TYPE[ty]['db_name'],
#         text=text,
#         editor=editor,
#         place_id=i
#     ).save()
#
#
# def handle_text_edit(update: Update, context: CallbackContext) -> None:
#     data = context.match.groups()[0]
#     user_id = update.effective_user.id
#
#     try:
#         decoded_data = json.loads(base64.b64decode(data, validate=True))
#
#         ty = int(decoded_data['ty'])
#         ticket = UUID(decoded_data['t'])
#         i = int(decoded_data['i'])
#
#         if not Editor.objects.filter(telegram_id=user_id).exists():
#             editor = Editor(telegram_id=user_id)
#             editor.save()
#         else:
#             editor = Editor.objects.get(telegram_id=user_id)
#
#         if not Edition.objects.filter(unique_id=ticket).exists():
#             _process_edition(ty, ticket, i, editor, update)
#
#             update.message.reply_text(
#                 text='Gracias por su contribución, se le notificará en caso de ser aceptada por los moderadores.'
#             )
#         else:
#             update.message.reply_text(
#                 text='Ya se realizó la contribución, '
#                      'para generar una nueva contribución por favor use el menú bajo el mensaje del lugar.'
#             )
#
#     except (binascii.Error, JSONDecodeError, UnicodeDecodeError, ValueError, KeyError) as e:
#         update.message.reply_text(
#             'Hubo un problema procesando su solicitud. Intente de nuevo.')
#         raise e
