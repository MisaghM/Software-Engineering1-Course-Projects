from django.contrib import admin
from .models import (
    Patient,
    OrganizationUser,
    HealthExpert,
    Document,
    HealthCenter,
    Doctor,
)

admin.site.register((Patient, OrganizationUser, HealthExpert, Document, HealthCenter, Doctor))
