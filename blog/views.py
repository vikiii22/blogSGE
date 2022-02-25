from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import FormularioPost  # importamos el formulario Post
from django.contrib import messages  # Para tratar los mensajes de error
from .models import Product
from django.contrib.auth.decorators import login_required  # Decorador para requerir la autenticacion


# Create your views here.

# @login_required(login_url='/accounts/acceder')
def index(request):
    # return HttpResponse("¡Hola, bienvenid@ al Blog!")
    products = Product.objects.all()
    return render(request, "blog.html", {"products": products})


@login_required(login_url='/accounts/acceder')
def crear_post(request):
    if request.method == "POST":  # comprobamos la petición
        # este formulario también recibe archivos
        # para procesarlos se han de incluirr
        form = FormularioPost(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)  # no guardamos de manera persistente porque nos falta el usuario
            # extraemos el usuario autenticado
            product.autor_id = request.user.id
            product.save()  # ahora sí que guardamos la información
            titulo = form.cleaned_data.get("titulo")
            messages.success(request, f"El product {titulo} se ha creado correctamente")
            return redirect("blog")
        else:  # si el formulario no es válido recorremos todos los mensajes y los devolvemos
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
    form = FormularioPost()  # aquí tendríamos el formulario
    return render(request, "crear_post.html", {"form": form})  # y se lo pasamos a la vista crear_post.html


@login_required(login_url='/accounts/acceder')
def eliminar_post(request, post_id):
    try:
        product = Product.objects.get(pk=post_id)  # recogemos el id del product de la url
    except Product.DoesNotExist:  # por si se accede a una url de un product que NO existe
        messages.error(request, "El product que quieres eliminar no existe.")
        return redirect("blog")

    # si no se origina la excepción, el product existe;
    # por lo que se habrá de comprobar que el product que se quiere eliminar
    # es del usuario que hace la petición
    if product.autor != request.user:
        messages.error(request, "No eres el autor de este product.")
        return redirect("blog")

    # Existe el product y es el autor: eliminamos
    product.delete()
    messages.success(request, F"El product {product.titulo} ha sido eliminado!")
    return redirect("blog")
