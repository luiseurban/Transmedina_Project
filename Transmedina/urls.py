from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('conductores.urls')),
    path('conductor/', include('conductor_dashboard.urls')),
]