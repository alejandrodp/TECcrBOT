from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from .models import Service


def service_builder(service: Service, reply):
    response = "\n\n".join((
        f"<i>Descripción:</i> \n{service.description if service.description else 'No disponible'}",
        f"<i>Contacto:</i> \n{service.contact if service.contact else 'No disponible'}"
    ))

    reply.text(
        response,
        reply_markup=InlineKeyboardMarkup.from_column([
            InlineKeyboardButton(f"Ir a {service.name}", url=service.link)
        ]) if service.link else None
    )
