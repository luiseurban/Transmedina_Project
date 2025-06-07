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
    