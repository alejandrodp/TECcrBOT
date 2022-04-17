from telegram.ext import CallbackContext

from tcrb.apps.pages_index.buttons import pagesty_paginator, pages_paginator, pagety_button, back_index
from tcrb.core.handlers import HandlerConfig, CallbackQueryHandler
from tcrb.pages.config import all_pages


def main_menu_handler(reply, context: CallbackContext):
    response = f"El apartado de índice le permite navegar la mayoría de la información disponible en el bot.\n\n" \
               f"Seleccione la página que desea ver:"

    markup = pagesty_paginator(1, list(all_pages.page_tys.values())).markup

    reply.text(response, reply_markup=markup)


def pagety_paginator_handler(reply, context: CallbackContext):
    current_page = reply.expect_int(context.match.group(1))

    markup = pagesty_paginator(current_page, list(all_pages.page_tys.values())).markup

    reply.edit_markup(markup)


def pagety_pages_handler(reply, context: CallbackContext):
    ty = reply.expect_int(context.match.group(1))
    build_pages_paginator(1, ty, reply)


def pagety_pages_paginator_handler(reply, context: CallbackContext):
    current_page = reply.expect_int(context.match.group(1))
    ty = reply.expect_int(context.match.group(2))
    build_pages_paginator(current_page, ty, reply)


def build_pages_paginator(page, ty, reply):
    paginator = pages_paginator(page, f"ty:{ty}", ty)
    paginator.add_after(back_index("Regresar al índice"))
    reply.edit_markup(paginator.markup)


PAGES_INDEX_HANDLERS = HandlerConfig([
    CallbackQueryHandler(pagesty_paginator, pagety_paginator_handler),
    CallbackQueryHandler(pagety_button, pagety_pages_handler),
    CallbackQueryHandler(pages_paginator, pagety_pages_paginator_handler),
    CallbackQueryHandler(back_index, main_menu_handler),
])
