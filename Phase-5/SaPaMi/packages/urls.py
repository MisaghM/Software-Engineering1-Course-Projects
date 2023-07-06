from django.urls import path
from . import views

urlpatterns = [
    path('packages/<int:id>', views.more_info, name='packages'),
    path('packages/<int:id>/reserve', views.reserve_package, name='reserve_package'),
    path('packages/<int:id>/confirm', views.confirm_reserve, name='confirm_reserve'),
    path('reservations', views.user_reservations, name='user_reservations'),
    path('reservations/<int:id>', views.user_reservation, name='user_reservation'),
]
