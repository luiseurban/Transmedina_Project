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

logger = logging.getLogger(__name__)

# Create your views here.


@login_required
def home(request):
    return render(request, 'pages/home/home.html')

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