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

    # 1. Gráfica: Novedades por tipo
    novedades_por_tipo = (
        Novedades.objects.values('tipo_novedad')
        .annotate(total=Count('id'))
        .order_by('tipo_novedad')
    )

    # 2. Filtros rápidos
    filtro_tipo = request.GET.get('tipo_novedad', '')
    filtro_fecha = request.GET.get('fecha', '')
    actividad_filtrada = Novedades.objects.select_related('mototaxi', 'conductor')
    if filtro_tipo:
        actividad_filtrada = actividad_filtrada.filter(tipo_novedad=filtro_tipo)
    if filtro_fecha:
        actividad_filtrada = actividad_filtrada.filter(fecha_novedad__date=filtro_fecha)
    actividad_filtrada = actividad_filtrada.order_by('-fecha_novedad')[:5]

    # 3. Indicadores adicionales
    conductores_sin_mototaxi = Conductores.objects.filter(mototaxi__isnull=True).count()
    mototaxis_sin_conductor = Mototaxis.objects.filter(conductores__isnull=True).count()
    novedades_resueltas = Novedades.objects.filter(tipo_novedad='ACTIVO').count()
    novedades_pendientes_count = Novedades.objects.exclude(tipo_novedad='ACTIVO').count()

    # 6. Alertas
    alertas = []
    if mototaxis_sin_conductor > 0:
        alertas.append(f"{mototaxis_sin_conductor} mototaxis sin conductor asignado.")
    if novedades_pendientes_count > 0:
        alertas.append(f"{novedades_pendientes_count} novedades pendientes.")
    if conductores_sin_mototaxi > 0:
        alertas.append(f"{conductores_sin_mototaxi} conductores sin mototaxi asignado.")

    return render(request, 'pages/home/home.html', {
        'total_mototaxis': total_mototaxis,
        'total_conductores': total_conductores,
        'total_novedades': total_novedades,
        'mototaxis_activas': mototaxis_activas,
        'novedades_activas': novedades_activas,
        'actividad_reciente': actividad_reciente,
        'novedades_pendientes': novedades_pendientes,
        'actividad_filtrada': actividad_filtrada,
        'novedades_por_tipo': list(novedades_por_tipo),
        'conductores_sin_mototaxi': conductores_sin_mototaxi,
        'mototaxis_sin_conductor': mototaxis_sin_conductor,
        'novedades_resueltas': novedades_resueltas,
        'novedades_pendientes_count': novedades_pendientes_count,
        'alertas': alertas,
        'filtro_tipo': filtro_tipo,
        'filtro_fecha': filtro_fecha,
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