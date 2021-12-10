from django.shortcuts import render, redirect
# clase vista de django
from django.views.generic import View
# formulario que provee django
from django.contrib.auth.forms import UserCreationForm

#nos permite crear sesiones flash
from django.contrib import messages
#funciones de login identificacion usuario
from django.contrib.auth import login

# la clase ViewRegistre está heredando de la clase View
class ViewRegistre(View):
    # recibir peticiones get y mostrar el formulario de registro
    def get(self, request):
        form = UserCreationForm()  # formulario vinculado con la tabla de BBDD
        return render(request, "registro.html", {"form": form})

    #recibir peticiones post y procesar el formulario de registro
    # noinspection PyMethodMayBeStatic
    def post(self, request):
        #pasamos los datos del formulario - POST - para que django los procese
        form = UserCreationForm(request.POST)
        #validamos el formulario
        if form.is_valid():
            #si es válido, crea un usuario en la tabla auth_user vinculada en el modelo
            usuario = form.save()
            #cleaned_data limpia valores y solo contiene los campos del formulario
            nombre = form.cleaned_data.get("username")
            #creamos una sesion flash cuando se da de alta un usuario
            #F o f formatea el mensaje de respuesta permitiendo introducir variable -- Antonio!
            messages.success(request, F"Bienvenid@ a nuestro blog {nombre}")
            #identificamos al usuario
            login(request, usuario)
            #una vez que ha iniciado sesion lo redirigimos al blog y sus entradas
            return redirect("blog") #hacemos cambio de las urls
        else:
            # msg recoge los mensajes de error
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])#extraemos el mensaje de error
            #si hay errores nos quedaremos en el formulario de registro
            return render(request, "registro.html", {"form": form})