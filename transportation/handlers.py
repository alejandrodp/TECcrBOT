from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext


from transportation import apps
from transportation.models import Vehicle, Route, Stop, Schedule
from .util import render_route

IKB = InlineKeyboardButton


def menu_entry(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        text="Seleccione un tipo de transporte:",
        reply_markup=InlineKeyboardMarkup.from_column(
            [
                IKB(vehicle.name,
                    callback_data=f"{apps.TransportationConfig.name}:vehicle:{vehicle.id}")
                for vehicle in Vehicle.objects.all()
            ]
        )
    )


def _build_routes(update, vehicle_id) -> None:
    update.message.reply_text(
        text="Seleccione una ruta:",
        reply_markup=InlineKeyboardMarkup.from_column(
            [
                IKB(f"{route.source} - {route.destination}",
                    callback_data=f"{apps.TransportationConfig.name}:route:{route.id}")
                for route in Route.objects.filter(vehicle_id=vehicle_id).order_by("source__name").all()
            ]
        )
    )


def get_routes(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    vehicle_id = query.data.split(':')[-1]

    if Vehicle.objects.filter(id=vehicle_id).exists():
        _build_routes(update, vehicle_id)
    else:
        query.message.edit_text(
            text="No existen rutas para este servicio de transporte."
        )


def get_schedule(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    route_id = query.data.split(':')[-1]

    response = "Esta ruta no existe."

    if Route.objects.filter(id=route_id).exists():
        route = Route.objects.get(id=route_id)

        response = render_route(route)

    query.message.edit_text(
        text=response
    )
