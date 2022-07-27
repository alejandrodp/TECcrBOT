from telegram import Message, InputMediaPhoto
from telegram.ext import CallbackContext

from tcrb.settings import BASE_DIR


def main_menu_handler(reply, context: CallbackContext) -> None:
    response = "(Última modificación: 25-07-2022)\n\n" \
               "Muy pronto estará disponible esta funcionalidad. " \
               "Podrá ver precios, horarios, próximas salidas y otra " \
               "información relevante. ¡Vuelva a revisar pronto!\n\n" \
               "Por el momento puede ver los horarios publicados por la FEITEC en" \
               "<a href='https://www.instagram.com/p/Cge1AgHur4w/'>Instagram</a>\n\n" \
               "Si desea contribuir a este proyecto puede contactar a @adiazp"

    message: Message = reply.text(response)

    message.reply_media_group([
        InputMediaPhoto(open('/home/alejandro/projects/tcrb/contrib/transportation/photos/sj.jpg', mode='rb')),
        InputMediaPhoto(open('/home/alejandro/projects/tcrb/contrib/transportation/photos/sj1.jpg', mode='rb'),
                        caption='San José - TEC')
    ])

    message.reply_media_group([
        InputMediaPhoto(open('/home/alejandro/projects/tcrb/contrib/transportation/photos/alajuela.jpg', mode='rb'),
                        caption='Alajuela - TEC')
    ])

    message.reply_media_group([
        InputMediaPhoto(open('/home/alejandro/projects/tcrb/contrib/transportation/photos/heredia.jpg', mode='rb'),
                        caption='Heredia - TEC')
    ])

    message.reply_media_group([
        InputMediaPhoto(open('/home/alejandro/projects/tcrb/contrib/transportation/photos/coronado.jpg', mode='rb')),
        InputMediaPhoto(open('/home/alejandro/projects/tcrb/contrib/transportation/photos/coronado1.jpg', mode='rb'),
                        caption='Coronado - TEC')
    ])
