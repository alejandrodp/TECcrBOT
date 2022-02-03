from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from services import apps
from services.models import Service

IKB = InlineKeyboardButton


def main_entry(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        text="Seleccione un servicio:",
        reply_markup=InlineKeyboardMarkup.from_column(
            [
                IKB(text=s.name,
                    callback_data=f'{apps.ServicesConfig.name}:selecting_service:{s.id}')
                for s in Service.objects.all()
            ]
        )
    )


def process_service(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    service_id = query.data.split(':')[-1]

    service = Service.objects.get(id=service_id)

    query.message.edit_text(
        text='Nombre: {name}'
             '\n\nDescripción:\n{desc}'
             '\n\nEnlace a la página oficial: {link}'
             '\n\nContactos:\n{cont}'.format(name=service.name,
                                             desc=service.description
                                             if service.description else "Descripción no disponible",
                                             link=service.link
                                             if service.link else "Enlace no disponible",
                                             cont=service.contact
                                             if service.contact else "Información de contacto no disponible"
                                             )
    )
