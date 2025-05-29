
from django.contrib import admin
from django.urls import path
from conductores import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name= 'home'),
    path('signup/', views.signup, name= 'signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    #CRUD CONDUCTORES
    path('conductores/', views.conductores_main_view, name= 'conductores'),
    path('conductores/create_conductor/',views.create_conductor , name = 'create_conductor'),
    path('conductores/<int:cedula>/', views.conductor_detail, name = 'conductor_detail'),
    path('conductores/<int:cedula>/delete', views.delete_conductor, name = 'delete_conductor'),
    #CRUD MOTOTAXI
    path('mototaxis/', views.mototaxis_main_view, name='mototaxis'),
    path('mototaxis/create_mototaxi/',views.create_mototaxi, name='create_mototaxi'),
    path('mototaxis/<str:placa_mototaxi>/', views.mototaxi_detail, name = 'mototaxi_detail'),
    path('mototaxis/<str:placa_mototaxi>/delete', views.delete_mototaxi, name = 'delete_mototaxi'),
    #CURD NOVEDADES
    path('novedades/', views.novedades_main_view, name='novedades'),
    path('novedades/create_novedad/', views.create_novedad, name='create_novedad'),
    path('about/', views.about, name='about'),
]
