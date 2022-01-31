from services.models import Service


def index():
    for service in Service.objects.all():
        yield {
            'id': service.id,
            'title': service.name,
        }
