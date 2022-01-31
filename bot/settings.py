from places.settings import MAIN_MENU_COMMAND as PLACES_COMMAND
from services.settings import MAIN_MENU_COMMAND as SERVICES_COMMAND
from transport.settings import MAIN_MENU_COMMAND as TRANSPORT_COMMAND
from tutorias.settings import MAIN_MENU_COMMAND as TUTORIALS_COMMAND

MAIN_MENU = [
    # ['Próximo Bus 🚍'],
    [TRANSPORT_COMMAND, SERVICES_COMMAND],
    [PLACES_COMMAND, TUTORIALS_COMMAND],
    ['Noticias TEC 📰', 'Correos ✉️'],
    ['Info 🤖']]

