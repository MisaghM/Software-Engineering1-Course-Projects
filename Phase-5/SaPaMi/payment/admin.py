from django.contrib import admin
from .models import (
    Bill,
    Payment,
    CreditCard,
)

admin.site.register((Bill, Payment, CreditCard))
