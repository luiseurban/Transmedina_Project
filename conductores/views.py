from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Conductores, Mototaxis, Novedades
from .forms import Conductor_Form, Mototaxi_Form, Novedad_Form
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import datetime
import logging
from django.db.models import Count

logger = logging.getLogger(__name__)

# Create your views here.


@login_required
def home(request):
    # Estadísticas principales
    total_mototaxis = Mototaxis.objects.count()
    total_conductores = Conductores.objects.count()
    total_novedades = Novedades.objects.count()
    mototaxis_activas = Mototaxis.objects.filter(conductores__isnull=False).distinct().count()
    novedades_activas = Novedades.objects.exclude(tipo_novedad='ACTIVO').count()

    # Actividad reciente (últimas 5 novedades)
    actividad_reciente = Novedades.objects.select_related('mototaxi', 'conductor').order_by('-fecha_novedad')[:5]

    # Novedades pendientes (no activas)
    novedades_pendientes = Novedades.objects.exclude(tipo_novedad='ACTIVO').order_by('-fecha_novedad')[:3]

    return render(request, 'pages/home/home.html', {
        'total_mototaxis': total_mototaxis,
        'total_conductores': total_conductores,
        'total_novedades': total_novedades,
        'mototaxis_activas': mototaxis_activas,
        'novedades_activas': novedades_activas,
        'actividad_reciente': actividad_reciente,
        'novedades_pendientes': novedades_pendientes,
    })

def signin(request):
    if request.method == 'GET':
        return render(request, 'pages/signin/signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'pages/signin/signin.html', {
                'form': AuthenticationForm, 'error': 'Nombre de usuario o contraseña incorrecta.'})
        else:
            login(request, user)
            return redirect('home')

def signup(request):

    if request.method == 'GET':
        return render(request, 'pages/signup/signup.html', {
            'form': UserCreationForm
        })

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # registrar al usuario si las contraseñas coinciden
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('conductores')
            except IntegrityError:
                return render(request, 'pages/signup/signup.html', {'form': UserCreationForm, "Error": 'el usuario ya existe'})

        else:
            return render(request, 'pages/signup/signup.html', {'form': UserCreationForm, "Error": 'Las contraseñas no coinciden'})

def signout(request):
    logout(request)
    return redirect('home')

def about(request):
    return render(request, 'pages/about_us/about.html')

def redirect_to_conductor_signin(request):
    return redirect('/conductor/conductor_signin/')