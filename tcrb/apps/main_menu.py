from telegram import ReplyKeyboardMarkup
from telegram.ext import Filters

from .config.handlers import HandlerConfig, MessageHandler, CommandHandler
from .places.handlers import main_menu_handler as places_main_menu
from .places.settings import PLACES_DESC
from .services.handlers import main_menu_handler as services_main_menu
from .services.settings import SERVICES_DESC
from .transportation.handlers import main_menu_handler as transportation_main_menu
from .transportation.settings import TRANSPORTATION_DESC
from .tutorias.handlers import main_menu_handler as tutorias_main_menu
from .tutorias.settings import TUTORIAS_DESC


def info_message_handler(reply, context) -> None:
    response = f"Este bot fue inicialmente creado por Esteban Sánchez Trejos, " \
               f"quien lo mantuvo desde 2017 hasta 2021, en conjunto con " \
               f"la asociación de estudiantes de la carrera de Mecatrónica (AEMTEC).\n\n" \
               f"A partir del 2021 cluster451 se incorporó en el desarrollo del proyecto.\n\n" \
               f"Cluster451 es un grupo enfocado en el software libre y la autonomía de datos, " \
               f"conformado actualmente por estudiantes del TEC de múltiples carreras.\n\n" \
               f"Si desea contribuir al proyecto, hacer sugerencias o comentarios, comunicarse con Fabián Montero (@fabianmv)."

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
               f"\U0001f539 Menú principal\n\n" \
               f"En este bot puede encontrar información acerca del TEC y sus servicios.\n" \
               f"Para realizar una consulta puede escribir términos como los siguientes:\n" \
               f"\U0001f68c Obtener información de buses:\n" \
               f"- buses\n" \
               f"- buses tec\n" \
               f"- buses san jose\n" \
               f"\U0001f4cd Obtener información de un lugar:\n" \
               f"- D3\n" \
               f"- F2\n" \
               f"- admision y registro\n" \
               f"\U0001f4d6 Obtener información de contacto:\n" \
               f"- secretaria quimica\n" \
               f"- docente <i>nombre o apellido del profesor</i>"

    reply.text(response,
               reply_markup=MAIN_MENU_HANDLERS.keyboard_markup()
               )


class MainMenuConfig(HandlerConfig):
    def __init__(self, entries):
        handlers = []
        self._main_menu = []
        for text, callback in entries.items():
            self._create_main_menu_entry(text)
            handlers.append(MessageHandler(Filters.text(text), callback))
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
