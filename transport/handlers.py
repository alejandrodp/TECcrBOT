from typing import List

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from common.constants import DAYS_MAPPING
from transport import apps
from transport.models import Vehicle, Trip, Schedule

IKB = InlineKeyboardButton


def menu_entry(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        text="Seleccione un tipo de transporte:",
        reply_markup=InlineKeyboardMarkup.from_column(
            [
                IKB(vehicle.name, callback_data=f"{apps.TransportConfig.name}:t_type:{vehicle.id}")
                for vehicle in Vehicle.objects.all()
            ]
        )
    )


def _build_travel_list(vehicle: str) -> List[IKB]:
    trip = []

    for trip in Vehicle.objects.get(id=vehicle).trip_set.order_by('start_location').all():
        text = '{start} -> {end}'.format(
            start=trip.start_location,
            end=trip.end_location
        )

        trip.append(IKB(text, callback_data=f"{apps.TransportConfig.name}:travel:{trip.id}"))

    return trip


def process_type(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    vehicle = query.data.split(':')[-1]

    if not Vehicle.objects.get(id=vehicle).trip_set.exists():
        query.message.edit_text(
            text="No existen trayectos para este servicio de transporte",
        )
        return

    query.message.edit_text(
        text="Seleccione un trayecto:",
        reply_markup=InlineKeyboardMarkup.from_column(
            _build_travel_list(vehicle)
        )
    )


def _build_schedule(travel: Trip):
    start_points = []

    for point in travel.tripstartpoint_set.all():
        schedules = []

        schedules.append(
            'De Lunes a Viernes:\n{times}'.format(
                times='\n'.join(
                    sorted(
                        set([f'{t.time}'
                             for t in Schedule.objects
                            .filter(day__in=range(1, 6))
                            .filter(travel_id=travel.id)
                            .filter(start_point_id=point.id)
                            .order_by('time')
                            .all()
                             ]))) if Schedule.objects
                    .filter(day__in=range(1, 6))
                    .filter(travel_id=travel.id)
                    .filter(start_point_id=point.id).exists() else "No hay servicio"
            )
        )

        schedules.append(
            _build_time_schedule(6, travel.id, point.id)
        )

        schedules.append(
            _build_time_schedule(7, travel.id, point.id)
        )

        start_points.append(
            'Lugar de partida: {start}\n\n{schedules}'.format(
                start=point.description,
                schedules='\n\n'.join(schedules)
            )
        )

    if not start_points:
        return "No existe información de horarios para este trayecto."

    return '\n\n'.join(start_points)


def _build_time_schedule(day_index, travel_id, start_point_id) -> str:
    return '{day_name}:\n{times}'.format(
        day_name=DAYS_MAPPING.get(day_index, 'Día desconocido'),
        times='\n'.join(
            set([f'{t.time}'
                 for t in Schedule.objects
                .filter(day=day_index)
                .filter(travel_id=travel_id)
                .filter(start_point_id=start_point_id)
                .order_by('time')
                .all()
                 ])) if Schedule.objects
            .filter(day=day_index)
            .filter(travel_id=travel_id)
            .filter(start_point_id=start_point_id).exists() else "No hay servicio"
    )


def process_travel(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    trip_id = query.data.split(':')[-1]

    trip = Trip.objects.get(id=trip_id)

    schedule = _build_schedule(trip)

    response = 'Servicio de {service}\nTrayecto: Desde {start} hasta {end}\n\n{schedule}'.format(
        service=trip.type.name,
        start=trip.start_location,
        end=trip.end_location,
        schedule=schedule
    )

    query.message.edit_text(
        text=response
    )
