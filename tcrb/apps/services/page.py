from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from .models import Service
from .settings import SERVICES_DESC
from ...pages import PageTy


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


SERVICES_PAGE = PageTy(ty=0, model=Service, desc=SERVICES_DESC, build=service_builder)