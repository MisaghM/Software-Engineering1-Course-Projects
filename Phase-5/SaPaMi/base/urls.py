from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cas/', views.cas, name='cas'),
    path('cas/login', views.cas_login, name='cas-login'),
    path('cas/logout', views.cas_logout, name='cas-logout'),
    path('cas/signup', views.cas_signup, name='cas-signup'),
]
