from services.models import Service


def index_services():
    for service in Service.objects.all():
        yield {
            'id': service.id,
            'title': service.name,
        }
