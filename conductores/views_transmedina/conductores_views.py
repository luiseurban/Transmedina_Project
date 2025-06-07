from django.contrib.auth.decorators import login_required
from ..models import Conductores
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from ..forms import Conductor_Form
from django.contrib import messages
from django.urls import reverse
# CRUD CONDUCTORES


@login_required
def conductores_main_view(request):
    # Verificar si el usuario es admin
    is_admin = request.user.is_staff
    lista_conductores = Conductores.objects.all().order_by('id')

    # Muestra n conductores por página
    paginator = Paginator(lista_conductores, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/ConductorPages/conductores_view/conductores_view.html', {
        'is_admin': is_admin,
        # 'lista_conductores': lista_conductores,
        'page_obj': page_obj, })


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
                    form.add_error(
                        'cedula', 'Ya existe un conductor con esta cédula.')
                    messages.error(
                        request, 'No se pudo modificar el conductor. La cédula ya está registrada.')
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
            messages.error(
                request, 'No se pudo modificar el conductor. Verifica los datos.')

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
