from .models import Service
from .page import service_builder
from tcrb.apps.config.pages import PageTy

SERVICES_DESC = "Servicios generales \U0001f3eb"

SERVICES_PAGE = PageTy(ty=0, model=Service, desc=SERVICES_DESC, build=service_builder)
