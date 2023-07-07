from django.urls import path
from . import views

urlpatterns = [
    path('packages/<int:id>', views.more_info, name='packages'),
    path('packages/<int:id>/reserve', views.reserve_package, name='reserve_package'),
    path('packages/<int:id>/confirm', views.confirm_service, name='confirm_service'),
    path('reservations', views.reservations, name='reservations'),
    path('reservations/<int:id>', views.reservation, name='reservation'),
]
