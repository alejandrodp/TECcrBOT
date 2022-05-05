import os

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tcrb.settings")
application = get_wsgi_application()

# TODO: hacer que retorne False si start_bot falla.
def start_bot():    
    call_command("start_bot")
    return True


def check_database():
    """
    call_command("makemigrations", "--check", verbosity=0)
    call_command("migrate", "--check", verbosity=3)

    print(make)
    print(migrate)

    return not (make and migrate)
    """
    return True
