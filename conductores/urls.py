from django.urls import path
from .views_transmedina import conductores_views, mototaxis_view, novedades_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    # CRUD CONDUCTORES
    path('conductores/', conductores_views.conductores_main_view, name='conductores'),
    path('conductores/create_conductor/', conductores_views.create_conductor, name='create_conductor'),
    path('conductores/<int:cedula>/', conductores_views.conductor_detail, name='conductor_detail'),
    path('conductores/<int:cedula>/delete', conductores_views.delete_conductor, name='delete_conductor'),
    # CRUD MOTOTAXI
    path('mototaxis/', mototaxis_view.mototaxis_main_view, name='mototaxis'),
    path('mototaxis/create_mototaxi/', mototaxis_view.create_mototaxi, name='create_mototaxi'),
    path('mototaxis/<str:placa_mototaxi>/', mototaxis_view.mototaxi_detail, name='mototaxi_detail'),
    path('mototaxis/<str:placa_mototaxi>/delete', mototaxis_view.delete_mototaxi, name='delete_mototaxi'),
    # CRUD NOVEDADES
    path('novedades/', novedades_views.novedades_main_view, name='novedades_main_view'),
    path('novedades/create_novedad/', novedades_views.create_novedad, name='create_novedad'),
    path('novedades/<int:id_novedad>/', novedades_views.novedad_detail, name='novedad_detail'),
    path('novedades/<int:id_novedad>/eliminar', novedades_views.delete_novedad, name='delete_novedad'),
    path('about/', views.about, name='about'),
]