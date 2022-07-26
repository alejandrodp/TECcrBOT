from telegram.ext import CallbackContext
def main_menu_handler(reply, context: CallbackContext) -> None:
    response = "(Última modificación: 25-07-2022)\n\n" \
               "Muy pronto estará disponible esta funcionalidad. " \
               "Podrá ver precios, horarios, próximas salidas y otra " \
               "información relevante. ¡Vuelva a revisar pronto!\n\n" \
               "Por el momento puede ver los horarios " \
               "<a href='https://www.facebook.com/photo/?fbid=5623408161011604&set=pcb.5552738358111645'>aquí</a>\n\n" \
               "Si desea contribuir a este proyecto puede contactar a @adiazp"
    reply.text(response)

