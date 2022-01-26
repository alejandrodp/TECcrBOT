from typing import List

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from common.constants import DAYS_MAPPING
from transport import apps
from transport.models import TravelType, Travel, Schedule

IKB = InlineKeyboardButton


def menu_entry(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        text="Seleccione un tipo de transporte:",
        reply_markup=InlineKeyboardMarkup.from_column(
            [
                IKB(travel_type.name, callback_data=f"{apps.TransportConfig.name}:t_type:{travel_type.id}")
                for travel_type in TravelType.objects.all()
            ]
        )
    )


def _build_travel_list(travel_type: str) -> List[IKB]:
    travels = []

    for travel in TravelType.objects.get(id=travel_type).travel_set.order_by('start').all():
        text = '{start} -> {end}'.format(
            start=travel.start,
            end=travel.end
        )

        travels.append(IKB(text, callback_data=f"{apps.TransportConfig.name}:travel:{travel.id}"))

    return travels


def process_type(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    travel_type = query.data.split(':')[-1]

    if not TravelType.objects.get(id=travel_type).travel_set.exists():
        query.message.edit_text(
            text="No existen trayectos para este servicio de transporte",
        )
        return

    query.message.edit_text(
        text="Seleccione un trayecto:",
        reply_markup=InlineKeyboardMarkup.from_column(
            _build_travel_list(travel_type)
        )
    )


def _build_schedule(travel: Travel):
    start_points = []

    for point in travel.travelstartpoint_set.all():
        schedules = []

        schedules.append(
            'De Lunes a Viernes:\n{times}'.format(
                times='\n'.join(
                    sorted(
                        set([f'{t.time}'
                             for t in Schedule.objects
                            .filter(day__day_index__in=range(1, 6))
                            .filter(travel_id=travel.id)
                            .filter(start_point_id=point.id)
                            .order_by('time')
                            .all()
                             ]))) if Schedule.objects
                    .filter(day__day_index__in=range(1, 6))
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
                .filter(day__day_index=day_index)
                .filter(travel_id=travel_id)
                .filter(start_point_id=start_point_id)
                .order_by('time')
                .all()
                 ])) if Schedule.objects
            .filter(day__day_index=day_index)
            .filter(travel_id=travel_id)
            .filter(start_point_id=start_point_id).exists() else "No hay servicio"
    )


def process_travel(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    travel_id = query.data.split(':')[-1]

    travel = Travel.objects.get(id=travel_id)

    schedule = _build_schedule(travel)

    response = 'Servicio de {service}\nTrayecto: Desde {start} hasta {end}\n\n{schedule}'.format(
        service=travel.type.name,
        start=travel.start,
        end=travel.end,
        schedule=schedule
    )

    query.message.edit_text(
        text=response
    )
