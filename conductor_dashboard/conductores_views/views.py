from django.shortcuts import render, redirect
from conductores.models import Conductores

def conductor_login(request):
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
    return render(request, "pages/signin/signin.html", {"error": error})

