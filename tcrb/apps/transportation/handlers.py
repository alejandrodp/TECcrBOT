from telegram.ext import CallbackContext


def main_menu_handler(reply, context: CallbackContext) -> None:
    response = "(Última modificación: 23-02-2022)\n\n" \
               "El servicio de bus del TEC no se encuentra disponible en este momento, " \
               "solo se está ofreciendo el siguiente servicio:\n\n" \
               "Servicio de buseta que sale del centro de Cartago hacia el TEC a las 7:20 a.m\n" \
               "Servicio de buseta que sale del TEC al centro de Cartago a las 4:40 p.m\n\n" \
               "<b>Mensaje de FEITEC:</b>\n" \
               "Hemos estado recibiendo muchas consultas con respecto al servicio de buses " \
               "por lo que hicimos un formulario para conocer la necesidad real del servicio " \
               "y así poder realizar una solicitud a la administración.\n\n" \
               "Fuente: https://www.instagram.com/p/CaEJWUWu4FI/?utm_medium=copy_link\n" \
               "Formulario: https://forms.office.com/r/vcFWCDDV4v"

    reply.text(response)
