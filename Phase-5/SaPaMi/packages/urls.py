from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>', views.more_info, name='packages'),
    path('<int:id>/reserve', views.reserve_package, name='reserve_package'),
]
