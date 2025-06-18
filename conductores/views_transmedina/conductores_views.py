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

    # KPIs para dashboard
    total_conductores = lista_conductores.count()
    mototaxis_asignados = lista_conductores.filter(mototaxi__isnull=False).count()
    conductores_sin_mototaxi = lista_conductores.filter(mototaxi__isnull=True).count()
    total_correos = lista_conductores.exclude(correo__isnull=True).exclude(correo__exact='').values('correo').distinct().count()
    ultimo_conductor_obj = lista_conductores.order_by('-fecha_de_creacion').first()
    ultimo_conductor = f"{ultimo_conductor_obj.nombre} {ultimo_conductor_obj.apellido}" if ultimo_conductor_obj else "-"
    ultima_actualizacion = ultimo_conductor_obj.fecha_de_creacion.strftime('%d/%m/%Y %H:%M') if ultimo_conductor_obj else "-"

    # Resumen de acciones recientes
    accion = None
    conductor_accion = None
    fecha_accion = None
    if 'accion' in request.session:
        accion = request.session.get('accion')
        conductor_accion = request.session.get('conductor_accion')
        fecha_accion = request.session.get('fecha_accion')
        # Limpiar después de mostrar
        del request.session['accion']
        del request.session['conductor_accion']
        del request.session['fecha_accion']

    # Muestra n conductores por página
    paginator = Paginator(lista_conductores, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/ConductorPages/conductores_view/conductores_view.html', {
        'is_admin': is_admin,
        'page_obj': page_obj,
        'total_conductores': total_conductores,
        'mototaxis_asignados': mototaxis_asignados,
        'conductores_sin_mototaxi': conductores_sin_mototaxi,
        'total_correos': total_correos,
        'ultimo_conductor': ultimo_conductor,
        'ultima_actualizacion': ultima_actualizacion,
        'accion': accion,
        'conductor_accion': conductor_accion,
        'fecha_accion': fecha_accion,
    })


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

            # Guardar acción en sesión
            request.session['accion'] = 'actualizado'
            request.session['conductor_accion'] = f"{conductor.nombre} {conductor.apellido}"
            from django.utils import timezone
            request.session['fecha_accion'] = timezone.now().strftime('%d/%m/%Y %H:%M')

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
    conductor = get_object_or_404(Conductores, cedula=cedula)
    if request.method == 'POST':
        nombre = conductor.nombre
        apellido = conductor.apellido
        conductor.delete()
        # Guardar acción en sesión
        request.session['accion'] = 'eliminado'
        request.session['conductor_accion'] = f"{nombre} {apellido}"
        from django.utils import timezone
        request.session['fecha_accion'] = timezone.now().strftime('%d/%m/%Y %H:%M')
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
