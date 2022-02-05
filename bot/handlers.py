import html

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

from common.util import is_int, send_unknown_error
from tcrb.core import BotAppConfig, PageTy

page_tys = PageTy.read_page_tys()


def main_menu(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Seleccione una opción:",
        reply_markup=ReplyKeyboardMarkup(
            BotAppConfig.get_main_menu(),
            resize_keyboard=True,
        )
    )


def show_page_handler(update: Update, context: CallbackContext) -> None:
    ty = context.match.group(1)
    page_id = context.match.group(2)
    update.callback_query.answer()

    if not is_int(ty, page_id):
        send_unknown_error(update.effective_chat)

    ty = int(ty)
    page_id = int(page_id)

    PageTy.show_page(page_id, ty, update)


# def search_handler(update: Update, context: CallbackContext) -> None:
#     msg = html.escape(update.message.text)
#
#     results = _search(msg)
#
#     if not results:
#         update.message.reply_text(
#             "Su búsqueda ha durado demasiado, intente con términos más simples")
#         return
#
#     if len(results) == 0:
#         update.message.reply_text(
#             f'No se encontraron resultados para <i>{msg}</i>')
#         return

    # if len(results) == 1:
    #     ty, pages = results.popitem()
    #     msg, page_buttons = page_tys[ty].page_builder(pages[0][0])
    #
    #     update.message.reply_text(
    #         text=msg,
    #         reply_markup=InlineKeyboardMarkup.from_column(page_buttons)
    #         if page_buttons else None
    #     )
    #     return
    #
    # text, buttons = build_results_menu(results, msg)
    #
    # update.message.reply_text(
    #     text=text,
    #     reply_markup=InlineKeyboardMarkup.from_column(buttons)
    # )

#
# def build_results_menu(results, msg):
#     if len(results) > 1:
#         text = f'Resultados para <i>{msg}</i>'
#         buttons = [
#             handlers.create_inline_button(f'{page_tys[ty].desc} ({len(pages)})', 'get_type_pages', str(ty))
#             for ty, pages in results.items()]
#     else:
#         ty, pages = results.popitem()
#         text = f'Resultados de {page_tys[ty].desc} para <i>{msg}</i>'
#         buttons = [
#             build_page_button(f'{page[1]}', ty, page[0])
#             for page in pages
#         ]
#
#     return text, buttons
#
#
# def type_handler(update: Update, context: CallbackContext) -> None:
#     cq = update.callback_query
#     cq.answer()
#     ent = cq.message.entities[0]
#     offset = ent.offset
#     lenght = ent.offset + ent.length
#     query = html.escape(cq.message.text[offset:lenght])
#     ty = int(context.match.group(1))
#
#     results = _search(query)
#
#     if len(results[ty]) == 1:
#         page_id, _ = results[ty][0]
#         _show_page(page_id, ty, update)
#         return
#
#     cq.message.edit_text(
#         text=f'Resultados de {page_tys[ty].desc} para <i>{query}</i>',
#         reply_markup=InlineKeyboardMarkup.from_column([
#             build_page_button(page[1], str(ty), str(page[0]))
#             for page in results[ty]
#         ])
#     )
#
#
#
#
