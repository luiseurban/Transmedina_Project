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

# CRUD CONDUCTORES
@login_required
def conductores_main_view(request):
    # Verificar si el usuario es admin
    is_admin = request.user.is_staff
    lista_conductores = Conductores.objects.all().order_by('id')
    
    paginator = Paginator(lista_conductores, 10)  # Muestra n conductores por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'pages/ConductorPages/conductores_view/conductores_view.html', {
        'is_admin': is_admin, 
        # 'lista_conductores': lista_conductores,
        'page_obj': page_obj,})

@login_required

def conductor_detail(request, cedula):
    conductor = get_object_or_404(Conductores, cedula=cedula)

    if request.method == 'POST':
        form = Conductor_Form(request.POST, instance=conductor)

        if form.is_valid():
            nueva_cedula = form.cleaned_data['cedula']

            # Verificamos si la cédula ha cambiado y si ya existe otro conductor con la nueva cédula
            if conductor.cedula != nueva_cedula:
                if Conductores.objects.filter(cedula=nueva_cedula).exists():
                    form.add_error('cedula', 'Ya existe un conductor con esta cédula.')
                    messages.error(request, 'No se pudo modificar el conductor. La cédula ya está registrada.')
                    return render(request, 'pages/ConductorPages/conductor_detail/conductor_detail.html', {
                        'conductor': conductor, 
                        'form': form
                    })

                # Si la cédula cambió y no hay duplicado, se actualiza
                conductor.cedula = nueva_cedula

            # Guardamos el formulario sin crear un nuevo registro
            form.save()

            # Enviamos mensaje de éxito
            messages.success(request, 'Conductor modificado con éxito.')

            # Redirigimos para evitar el reenvío del formulario con F5
            return redirect('conductor_detail', cedula=conductor.cedula)

        else:
            messages.error(request, 'No se pudo modificar el conductor. Verifica los datos.')

    else:
        form = Conductor_Form(instance=conductor)

    return render(request, 'pages/ConductorPages/conductor_detail/conductor_detail.html', {
        'conductor': conductor, 
        'form': form
    })


@login_required
def delete_conductor(request, cedula):
    # Obtén el conductor con la cédula proporcionada (usando la cédula como pk)
    conductor = get_object_or_404(Conductores, cedula=cedula)

    # Si el método de la solicitud es POST, eliminamos el conductor
    if request.method == 'POST':
        # Eliminar el conductor
        conductor.delete()
        # Redirige a la lista de conductores después de eliminar
        return redirect('conductores')

@login_required
def create_conductor(request):
    if request.method == 'POST':
        form = Conductor_Form(request.POST)

        if form.is_valid():
            # Guardar el nuevo conductor si todas las validaciones son correctas
            create_conductor1 = form.save(commit=False)
            create_conductor1.user = request.user
            create_conductor1.save()

            # Redirigir a la vista de conductores con un mensaje de éxito
            return redirect(reverse('create_conductor') + '?success=true')

        else:
            # Aquí se maneja el caso de que el formulario no sea válido
            return render(request, 'pages/ConductorPages/create_conductor/create_conductor.html', {
                'form': form,
                'error': 'Errores de validación: Verifique los datos ingresados.',
                # Obtiene el mensaje de error específico de la cédula
                'cedula_error': form.errors.get('cedula', None),
            })
    else:
        form = Conductor_Form()

    return render(request, 'pages/ConductorPages/create_conductor/create_conductor.html', {'form': form})

# CRUD MOTOTAXIS
@login_required
def mototaxis_main_view(request):
    is_admin = request.user.is_staff
    lista_mototaxis = Mototaxis.objects.all().order_by('id')
    
    paginator = Paginator(lista_mototaxis, 10)  # Muestra n mototaxis por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pages/MotoTaxiPages/mototaxi_view/mototaxis_view.html', {
        'is_admin': is_admin, 
        'page_obj': page_obj,})

@login_required
def create_mototaxi(request):
    if request.method=='POST':
        form = Mototaxi_Form(request.POST)
        if form.is_valid():
            create_mototaxi1 = form.save(commit=False)
            create_mototaxi1.save()
            return redirect(reverse('create_mototaxi') + '?success=true')
        else:
            return render(request, 'pages/MotoTaxiPages/create_mototaxi/create_mototaxi.html', {
                    'form': form,
                    'error': 'Errores de validación: Verifique los datos ingresados.',
                    # Obtiene el mensaje de error específico de la cédula
                    'placa_mototaxi_error': form.errors.get('placa_mototaxi', None),
                })
    else:
        form = Mototaxi_Form()
    return render(request, 'pages/MotoTaxiPages/create_mototaxi/create_mototaxi.html', {'form': form})

@login_required
def mototaxi_detail(request, placa_mototaxi):
        # Obtenemos el conductor con la cédula proporcionada
    mototaxi = get_object_or_404(Mototaxis, placa_mototaxi=placa_mototaxi)

    if request.method == 'POST':
        form = Mototaxi_Form(request.POST, instance=mototaxi)

        if form.is_valid():
            nueva_placa_mototaxi = form.cleaned_data['placa_mototaxi']

            # Verificamos si la placa ha cambiado y si ya existe otro mototaxi con la nueva placa
            if mototaxi.placa_mototaxi != nueva_placa_mototaxi:
                if Conductores.objects.filter(placa_mototaxi=nueva_placa_mototaxi).exists():
                    # Si existe un mototaxi con la nueva cédula, mostramos un error
                    form.add_error(
                        'placa_mototaxi', 'Ya existe un mototaxi con esta placa.')
                    return render(request, 'pages/MotoTaxiPages/mototaxi_detail/mototaxi_detail.html', {'mototaxi': mototaxi, 'form': form, 'error': 'La placa ya está registrada.'})
                # Si la placa cambió y no existe un duplicado, actualizamos la placa
                mototaxi.placa_mototaxi = nueva_placa_mototaxi
            # Guardamos el formulario sin crear un nuevo registro, solo actualizando el mototaxi existente
            form.save()
            # Redirigimos a la lista de mototaxis después de la actualización
            return redirect('mototaxis')
        else:
            return render(request, 'pages/MotoTaxiPages/mototaxi_detail/mototaxi_detail.html', {'mototaxi': mototaxi, 'form': form, 'error': 'Errores de validación.'})

    form = Mototaxi_Form(instance=mototaxi)
    return render(request, 'pages/MotoTaxiPages/mototaxi_detail/mototaxi_detail.html', {'mototaxi': mototaxi, 'form': form})

@login_required
def delete_mototaxi(request, placa_mototaxi):
    # Obtén el mototaxi con el id proporcionada (usando el id como pk)
    mototaxi = get_object_or_404(Mototaxis, placa_mototaxi=placa_mototaxi)

    # Si el método de la solicitud es POST, eliminamos el mototaxi
    if request.method == 'POST':
        # Eliminar el mototaxi
        mototaxi.delete()
        # Redirige a la lista de mototaxis después de eliminar
        return redirect('mototaxis')
    
#CRUD NOVEDADES
@login_required
def novedades_main_view(request):
      #Obtener párametros del GET
    tipo_novedad = request.GET.get('tipo_novedad', "todos")
    conductor_id = request.GET.get('conductor', "todos")
    ordenar_tipo = request.GET.get('ordenar_tipo', "")
    ordenar_conductor = request.GET.get('ordenar_conductor', "")
    
    novedades = Novedades.objects.all()

    #Filtro por tipo de novedad
    if tipo_novedad and tipo_novedad != "todos":
        novedades = novedades.filter(tipo_novedad=tipo_novedad)

    #Filtro por conductor
    if conductor_id and conductor_id != "todos":
        try:
          conductor_id = int(conductor_id)
          novedades = novedades.filter(conductor_id=int(conductor_id))    
        except ValueError:
            pass #Ignora si no es un número

    #Ordenar por tipo de novedad
    if ordenar_tipo == "reciente":
        novedades = novedades.order_by('-id')
    elif ordenar_tipo == "antiguo":
        novedades = novedades.order_by('id')
    
    #Ordenar por conductor
    if ordenar_conductor == "asc":
        novedades = novedades.order_by('conductor__nombre') 
    elif ordenar_conductor == "desc":
        novedades = novedades.order_by('-conductor__nombre')
    elif ordenar_conductor == "recientes":
        novedades = novedades.order_by('-conductor__fecha_de_creacion')
    
    #Obtener la lista única de tipos de novedad para el filtro
    tipos_novedad = Novedades.ESTADOS

    

    return render(request, 'pages/NovedadesPages/novedades_main_view/novedades_main_view.html', {
        'novedades': novedades,
        'tipos_novedad': tipos_novedad,
        'conductores': Conductores.objects.all(),
        'tipo_novedad_seleccionado': tipo_novedad,
        'conductor_seleccionado': conductor_id,
        'ordenar_tipo': ordenar_tipo,
        'ordenar_conductor': ordenar_conductor,
        'is_admin': True,
    })

@login_required
def create_novedad(request):
    if request.method == 'POST':
        form = Novedad_Form(request.POST)

        if form.is_valid():

            create_novedad1 = form.save(commit=False)
            create_novedad1.user = request.user
            create_novedad1.save()
            
            messages.success(request, 'Novedad registrada con éxito.')
            return redirect(reverse('create_novedad') + '?success=true')
        else:
            # Log form errors for debugging
            logger.error(f"Form errors: {form.errors}")
            messages.error(request, 'No se pudo registrar la novedad. Verifique los datos ingresados.')
    else:
        form = Novedad_Form()
    return render(request, 'pages/NovedadesPages/create_novedad/create_novedad.html', {'form': form})


def about(request):
    return render(request, 'pages/about_us/about.html')