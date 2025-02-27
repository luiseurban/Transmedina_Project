from django.forms import ModelForm
from .models import Conductores, Mototaxis
from django import forms


class Conductor_Form(forms.ModelForm):
    class Meta:
        model = Conductores
        fields = ['cedula', 'nombre', 'apellido', 'usuario', 'password', 'correo', 'mototaxi']

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        
        # Validar la cédula solo si el formulario es nuevo o si se está cambiando la cédula
        if self.instance and self.instance.pk:
            # Si estamos actualizando, revisar si hay otro conductor con la nueva cédula
            if Conductores.objects.filter(cedula=cedula).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Ya existe un conductor con esta cédula.")
        else:
            # Si estamos creando un conductor, asegurarnos de que la cédula no exista
            if Conductores.objects.filter(cedula=cedula).exists():
                raise forms.ValidationError("Ya existe un conductor con esta cédula.")

        return cedula

class Mototaxi_Form(forms.ModelForm):
    class Meta:
        model = Mototaxis
        fields = ['placa_mototaxi', 'modelo', 'marca']
    
    def clean_placa_mototaxi(self):
        
        placa_mototaxi = self.cleaned_data.get('placa_mototaxi')
        # Validar la placa solo si el formulario es nuevo o si se está cambiando la cédula
        if self.instance and self.instance.pk:
            # Si estamos actualizando, revisar si hay otro conductor con la nueva cédula
            if Mototaxis.objects.filter(placa_mototaxi=placa_mototaxi).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Ya existe un mototaxi con esta placa.")
        else:
            # Si estamos creando un conductor, asegurarnos de que la cédula no exista
            if Mototaxis.objects.filter(placa_mototaxi=placa_mototaxi).exists():
                raise forms.ValidationError("Ya existe un mototaxi con esta placa.")

        return placa_mototaxi