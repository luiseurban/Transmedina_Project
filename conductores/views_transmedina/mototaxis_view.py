from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from ..models import Conductores, Mototaxis
from ..forms import Mototaxi_Form
from django.urls import reverse

# CRUD MOTOTAXIS
@login_required
def mototaxis_main_view(request):
    is_admin = request.user.is_staff
    lista_mototaxis = Mototaxis.objects.all().order_by('id')

    # KPIs para dashboard
    total_mototaxis = lista_mototaxis.count()
    marcas_distintas = lista_mototaxis.values('marca').distinct().count()
    modelos_distintos = lista_mototaxis.values('modelo').distinct().count()
    mototaxis_asignados = lista_mototaxis.filter(conductores__isnull=False).count() if hasattr(Mototaxis, 'conductores') else 0

    # Último mototaxi creado
    ultimo_mototaxi_obj = lista_mototaxis.order_by('-id').first()
    ultimo_mototaxi = f"{ultimo_mototaxi_obj.placa_mototaxi} ({ultimo_mototaxi_obj.marca})" if ultimo_mototaxi_obj else "-"
    fecha_ultimo_mototaxi = ultimo_mototaxi_obj.id if ultimo_mototaxi_obj else "-"

    # Resumen de acciones recientes
    accion = request.session.pop('accion_mototaxi', None)
    mototaxi_accion = request.session.pop('mototaxi_accion', None)
    fecha_accion = request.session.pop('fecha_accion_mototaxi', None)

    paginator = Paginator(lista_mototaxis, 10)  # Muestra n mototaxis por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pages/MotoTaxiPages/mototaxi_view/mototaxis_view.html', {
        'is_admin': is_admin,
        'page_obj': page_obj,
        'total_mototaxis': total_mototaxis,
        'marcas_distintas': marcas_distintas,
        'modelos_distintos': modelos_distintos,
        'mototaxis_asignados': mototaxis_asignados,
        'ultimo_mototaxi': ultimo_mototaxi,
        'accion': accion,
        'mototaxi_accion': mototaxi_accion,
        'fecha_accion': fecha_accion,
    })

@login_required
def create_mototaxi(request):
    if request.method=='POST':
        form = Mototaxi_Form(request.POST)
        if form.is_valid():
            create_mototaxi1 = form.save(commit=False)
            create_mototaxi1.save()
            # Guardar acción en sesión
            request.session['accion_mototaxi'] = 'creado'
            request.session['mototaxi_accion'] = create_mototaxi1.placa_mototaxi
            from django.utils import timezone
            request.session['fecha_accion_mototaxi'] = timezone.now().strftime('%d/%m/%Y %H:%M')
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
            # Guardar acción en sesión
            request.session['accion_mototaxi'] = 'actualizado'
            request.session['mototaxi_accion'] = mototaxi.placa_mototaxi
            from django.utils import timezone
            request.session['fecha_accion_mototaxi'] = timezone.now().strftime('%d/%m/%Y %H:%M')
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
        placa = mototaxi.placa_mototaxi
        # Eliminar el mototaxi
        mototaxi.delete()
        # Guardar acción en sesión
        request.session['accion_mototaxi'] = 'eliminado'
        request.session['mototaxi_accion'] = placa
        from django.utils import timezone
        request.session['fecha_accion_mototaxi'] = timezone.now().strftime('%d/%m/%Y %H:%M')
        # Redirige a la lista de mototaxis después de eliminar
        return redirect('mototaxis')
