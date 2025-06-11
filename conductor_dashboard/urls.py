from django.urls import path
from .dashboard_views import dashboard_views

urlpatterns = [
    path('conductor_signin/', dashboard_views.conductor_signin, name='conductor_signin' ),
    path('dashboard_home/', dashboard_views.conductor_dashboard_home, name='conductor_dashboard_home'),
]