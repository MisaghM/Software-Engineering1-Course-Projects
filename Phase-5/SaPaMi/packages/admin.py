from django.contrib import admin
from .models import (
    Reservation,
    TherapeuticPackage,
    Service,
    TherapeuticService,
    ServiceRecord,
)

admin.site.register((Reservation, TherapeuticPackage, Service, TherapeuticService, ServiceRecord))
