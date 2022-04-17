from telegram import ReplyKeyboardMarkup
from telegram.ext import Filters

from .pages_index.handlers import main_menu_handler as pages_index_main_menu
from .pages_index.settings import PAGES_INDEX_DESC
from .search.handlers import main_menu_handler as search_main_menu
from .search.settings import SEARCH_DESC
from .tutorias.handlers import main_menu_handler as tutorias_main_menu
from .tutorias.settings import TUTORIAS_DESC
from ..core.handlers import HandlerConfig, CommandHandler, MessageHandler


def info_message_handler(reply, context) -> None:
    response = f"TECcrBot (TCRB) es un bot dedicado a proporcionar información y " \
               f"utilidades a los integrantes de la comunidad del ITCR.\n\n" \
               f"Creado por Esteban Sánchez Trejos, quién en conjunto con la asociación " \
               f"de estudiantes de la carrera de mecatrónica (AEMTEC) " \
               f"lo desarrolló durante 2017-2021.\n" \
               f"Actualmente Cluster451 mantiene el proyecto.\n\n" \
               f"<a href='https://www.cluster451.org/'>Cluster451</a> es un grupo enfocado en el software libre y " \
               f"la autonomía de datos, " \
               f"conformado actualmente por estudiantes del TEC de múltiples carreras.\n\n" \
               f"Si desea contribuir al proyecto, hacer sugerencias o comentarios, puede contactar a @adiazp.\n" \
               f"Puede encontrar el código de este bot <a href='https://git.cluster451.org/cluster451/tcrb'>aquí</a>"

    reply.text(response)


def main_menu_keyboard_handler(reply, context) -> None:
    reply.text(
        "Seleccione una opción:",
        reply_markup=MAIN_MENU_HANDLERS.keyboard_markup()
    )


def greetings_message_handler(reply, context) -> None:
    response = f"¡Hola {reply.user_first_name()}!\n" \
               f"Puede preguntar a través de:\n" \
               f"\U0001f539 Mensajes\n" \
               f"\U0001f539 Menú principal (presione aquí /menu)\n\n" \
               f"En este bot puede encontrar información acerca del TEC y sus servicios.\n" \
               f"Para realizar una consulta puede escribir términos como los siguientes:\n" \
               f"\U0001f4cd Obtener información de un lugar:\n" \
               f"- D3\n" \
               f"- F2\n" \
               f"- admision y registro\n" \
               f"\U0001f4d6 Obtener información de contacto:\n" \
               f"- secretaria quimica\n" \
               f"- nombre y/o apellido del profesor"

    reply.text(response,
               reply_markup=MAIN_MENU_HANDLERS.keyboard_markup()
               )


class MainMenuConfig(HandlerConfig):
    def __init__(self, entries):
        handlers = []
        self._main_menu = []
        for text, callback in entries.items():
            self._create_main_menu_entry(text)
            handlers.append(MessageHandler(Filters.text([text]), callback))
        super().__init__(handlers)

    def _create_main_menu_entry(self, text):
        if not self._main_menu or len(self._main_menu[-1]) >= 2:
            self._main_menu.append([])
        self._main_menu[-1].append(text)

    def keyboard_markup(self):
        return ReplyKeyboardMarkup(
            self._main_menu,
            resize_keyboard=True,
        )


MAIN_MENU_HANDLERS = MainMenuConfig({
    SEARCH_DESC: search_main_menu,
    PAGES_INDEX_DESC: pages_index_main_menu,
    TUTORIAS_DESC: tutorias_main_menu,
    "Info️ \U00002139": info_message_handler,
})

COMMAND_HANDLERS = HandlerConfig([
    CommandHandler("menu", main_menu_keyboard_handler),
    CommandHandler("start", greetings_message_handler),
    CommandHandler("help", greetings_message_handler),
])
