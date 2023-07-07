from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cas/', views.cas, name='cas'),
    path('cas/logout', views.cas_logout, name='cas_logout'),
]
