from django.contrib import admin
from django.urls import path, include

handler404 = 'base.views.my404'
handler403 = 'base.views.my403'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('', include('packages.urls')),
]
