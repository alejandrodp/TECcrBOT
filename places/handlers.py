from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackContext

from bot.buttons import page_button
from bot.menu import HandlerMaster
from common.util import Reply
from places.apps import PlacesConfig
from places.buttons import list_categories, list_categories_paginator, list_places, list_places_paginator
from places.constants import PAGE_TY
from places.models import Tag, Place

handlers = HandlerMaster(PlacesConfig.name)


def menu_entry(reply: Reply, context: CallbackContext) -> None:
    reply.text(
        "En esta sección puede ver todas las ubicaciones disponibles por categorías.\n"
        "También puede buscar una ubicación escribiendo el nombre (Ejemplos: A1, fotocopiadora)",
        reply_markup=InlineKeyboardMarkup.from_column(
            [
                list_categories.build_button("Ver categorías")
            ]
        )
    )


def first_category_list(reply: Reply, context: CallbackContext) -> None:
    send_category_list(1, reply.callback_query())


def remain_category_list(reply: Reply, context: CallbackContext) -> None:
    current_page = reply.expect_int(context.match.group(1))
    send_category_list(current_page, reply.callback_query())


def send_category_list(current_page_num, query):
    paginator = list_categories_paginator.build_paginator(
        current_page_num,
        Tag.objects.order_by('name').all(),
        lambda o: (list_places.build_button(tag.name, tag.id) for tag in o)
    )

    query.edit_message_text(
        text="Seleccione una categoría:",
        reply_markup=paginator.markup
    )


def first_place_list(reply: Reply, context: CallbackContext) -> None:
    tag_id = reply.expect_int(context.match.group(1))
    send_page_list(1, reply.callback_query(), tag_id)


def remain_place_list(reply: Reply, context: CallbackContext) -> None:
    current_page = reply.expect_int(context.match.group(1))
    tag_id = reply.expect_int(context.match.group(2))
    send_page_list(current_page, reply.callback_query(), tag_id)


def send_page_list(current_page, query, tag_id):
    paginator = list_places_paginator.build_paginator(
        current_page,
        Place.objects
        .filter(placetagged__tag_id=tag_id)
        .order_by('name').all(),
        lambda o:
        (page_button.build_button(place.name, PAGE_TY, place.id)
         for place in o),
        tag_id
    )

    query.edit_message_text(
        text="Seleccione una ubicación:",
        reply_markup=paginator.markup
    )
