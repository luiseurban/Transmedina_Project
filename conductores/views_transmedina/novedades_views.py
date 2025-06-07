from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..forms import Novedad_Form
from ..models import Novedades, Conductores
from django.contrib import messages
from datetime import datetime
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)


#CRUD NOVEDADES
@login_required
def novedades_main_view(request):
      #Obtener párametros del GET
    tipo_novedad = request.GET.get('tipo_novedad', "todos")
    conductor_id = request.GET.get('conductor', "todos")
    ordenar_tipo = request.GET.get('ordenar_tipo', "")
    ordenar_conductor = request.GET.get('ordenar_conductor', "")
    fecha_desde = request.GET.get('fecha_desde', "")
    fecha_hasta = request.GET.get('fecha_hasta', "")
    
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

    #Filtro por fecha
    if fecha_desde:
        try:
            fecha_obj = datetime.strptime(fecha_desde, '%Y-%m-%d')
            novedades = novedades.filter(fecha_novedad__gte=fecha_obj)
        except ValueError:
            pass
    if fecha_hasta:
        try:
            fecha_obj = datetime.strptime(fecha_hasta, '%Y-%m-%d')
            novedades = novedades.filter(fecha_novedad__lte=fecha_obj)
        except ValueError:
            pass

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
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta,
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

@login_required
def novedad_detail(request, id_novedad):
    novedad = get_object_or_404(Novedades, id=id_novedad)
    
    return render(request, 'pages/NovedadesPages/novedad_detail/novedad_detail.html', {
        'novedad': novedad,
    })

@login_required
def delete_novedad(request, id_novedad):
    novedad = get_object_or_404(Novedades, id=id_novedad)

    if request.method == 'POST':
        novedad.delete()
        messages.success(request, 'Novedad eliminada correctamente.')
        return redirect('novedades_main_view')

    return render(request, 'pages/NovedadesPages/novedad_confirm_delete.html', {
        'novedad': novedad
    })
