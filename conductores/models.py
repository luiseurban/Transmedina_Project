from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.hashers import make_password
# Create your models here.


class Mototaxis(models.Model):
    
    placa_mototaxi = models.CharField(max_length=10, unique=True)
    modelo = models.CharField(max_length=20)
    marca = models.CharField(max_length=20)
    
    def __str__(self):
        return self.placa_mototaxi  


class Conductores(models.Model):
    
    cedula = models.IntegerField(unique=True )
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    usuario = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    fecha_de_creacion = models.DateTimeField(default=timezone.now,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mototaxi = models.ForeignKey(Mototaxis, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self): 
        return self.cedula
  
class Novedades(models.Model):

    titulo_novedad = models.CharField(max_length=50)
    tipo_novedad = models.CharField(max_length=500)
    mototaxi = models.ForeignKey(Mototaxis, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self): 
        return self.titulo_novedad  