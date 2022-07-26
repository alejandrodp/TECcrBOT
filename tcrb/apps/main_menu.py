from telegram import ReplyKeyboardMarkup
from telegram.ext import Filters

from .places.settings import PLACES_DESC
from .places.handlers import main_menu_handler as places_main_menu
from .services.settings import SERVICES_DESC
from .services.handlers import main_menu_handler as services_main_menu
from .transportation.settings import TRANSPORTATION_DESC
from .transportation.handlers import main_menu_handler as transportation_main_menu
from .tutorias.handlers import main_menu_handler as tutorias_main_menu
from .tutorias.settings import TUTORIAS_DESC
from ..core.handlers import HandlerConfig, CommandHandler, MessageHandler


def info_message_handler(reply, context) -> None:
    """
    Mensaje mostrado cuando el usuario apreta el botón de información.
    """
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
    """
    Mensaje que se muestra la primera vez que se inicia el bot.
    """
    response =  f"¡Hola {reply.user_first_name()}!\n\n" \
                f"Para obtener información, podés escribir mensajes así:\n" \
                f"- D3\n" \
                f"- Admisión y registro\n" \
                f"- Secretaria química\n" \
                f"- Juan Pérez\n" \
                f"El bot va a tratar de interpretar tu mensaje y darte la mejor\n" \
                f"información disponible.\n\n" \
                f"Además, podés usar el Menú Principal para navegar por el índice\n" \
                f"y encontrar la información que necesitás."

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
    PLACES_DESC: places_main_menu,
    TRANSPORTATION_DESC: transportation_main_menu,
    SERVICES_DESC: services_main_menu,
    TUTORIAS_DESC: tutorias_main_menu,
    "Info️ \U00002139": info_message_handler,
})

COMMAND_HANDLERS = HandlerConfig([
    CommandHandler("menu", main_menu_keyboard_handler),
    CommandHandler("start", greetings_message_handler),
    CommandHandler("help", greetings_message_handler),
])
