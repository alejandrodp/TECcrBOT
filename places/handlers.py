from django.core.paginator import Paginator
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from bot.menu import build_page_button, BotHandler
from common.constants import PAGINATION_LIMIT
from common.util import is_int, send_unknown_error
from places.apps import PlacesConfig
from places.constants import States, PAGE_TY
from places.models import Tag, Place

handlers = BotHandler(PlacesConfig.name)


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

    if not is_int(current_page):
        send_unknown_error(update.effective_chat)
        return

    current_page = int(current_page)

    send_category_list(current_page, query)


def send_category_list(current_page_num, query):
    pages = Paginator(Tag.objects.order_by('name').all(), PAGINATION_LIMIT)

    current_pages = pages.get_page(current_page_num)

    buttons = [handlers.build_inline_button(tag.name, States.GET_PLACES, tag.id)
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


def first_place_list(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    tag_id = context.match.group(1)

    if not is_int(tag_id):
        send_unknown_error(update.effective_chat)
        return

    tag_id = int(tag_id)

    send_page_list(1, query, tag_id)


def remain_place_list(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    current_page = context.match.group(1)
    tag_id = context.match.group(2)

    if not (is_int(current_page) and is_int(tag_id)):
        send_unknown_error(update.effective_chat)
        return

    current_page = int(current_page)
    tag_id = int(tag_id)

    send_page_list(current_page, query, tag_id)


def send_page_list(current_page_num, query, tag_id):
    pages = Paginator(Place.objects
                      .filter(placetagged__tag_id=tag_id)
                      .order_by('name').all(),
                      PAGINATION_LIMIT)

    current_pages = pages.get_page(current_page_num)

    buttons = [build_page_button(place.name, PAGE_TY, place.id)
               for place in current_pages.object_list]

    paginator = handlers.build_paginator(
        current_page_num,
        States.GET_PLACE,
        pages,
        buttons,
        tag_id
    )

    query.edit_message_text(
        text="Seleccione una ubicación:",
        reply_markup=paginator.markup
    )
