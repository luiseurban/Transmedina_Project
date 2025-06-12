from django.shortcuts import render, redirect
from conductores.models import Conductores

def conductor_signin(request):
    error = None
    if request.method == "POST":
        usuario = request.POST.get("usuario")
        password = request.POST.get("password")
        try:
            conductor = Conductores.objects.get(usuario=usuario)
            if conductor.check_password(password):
                # Guardar el ID del conductor en la sesión
                request.session['conductor_id'] = conductor.id
                return redirect('conductor_dashboard_home')  # Cambia esto por la URL de inicio del dashboard de conductor
            else:
                error = "Contraseña incorrecta"
        except Conductores.DoesNotExist:
            conductor = None
            error = "Usuario no encontrado"
    return render(request, "pages/signin/signin_dashboard.html", {"error": error})

def conductor_logout(request):
    request.session.pop('conductor_id', None)
    return redirect('/conductor/conductor_signin/')

def conductor_dashboard_home(request):
    # Verifica si el conductor está autenticado por sesión
    if not request.session.get('conductor_id'):
        return redirect('/conductor/conductor_signin/')
    # ... lógica de la vista ...
    return render(request, 'pages/dashboard/dashboard_home.html')

