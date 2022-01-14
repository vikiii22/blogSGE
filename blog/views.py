from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import FormularioPost #importamos el formulario Post
from django.contrib import messages #Para tratar los mensajes de error
from .models import Post
# Create your views here.

def index(request):
    #return HttpResponse("¡Hola, bienvenid@ al Blog!")
    posts = Post.objects.all()
    return render(request, "blog.html", {"posts": posts})


def crear_post(request):
    if request.method == "POST": #comprobamos la petición
        # este formulario también recibe archivos
        # para procesarlos se han de incluir
        form = FormularioPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)#no guardamos de manera persistente porque nos falta el usuario
            #extraemos el usuario autenticado
            post.autor_id = request.user.id
            post.save()#ahora sí que guardamos la información
            titulo = form.cleaned_data.get("titulo")
            messages.success(request, f"El post {titulo} se ha creado correctamente")
            return redirect("blog")
        else:#si el formulario no es válido recorremos todos los mensajes y los devolvemos
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
    form = FormularioPost()#aquí tendríamos el formulario
    return render(request, "crear_post.html", {"form": form})#y se lo pasamos a la vista crear_post.html

def eliminar_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id) # recogemos el id del post de la url
    except Post.DoesNotExist: # por si se accede a una url de un post que NO existe
        messages.error(request, "El post que quieres eliminar no existe.")
        return redirect("blog")

    # si no se origina la excepción, el post existe;
    # por lo que se habrá de comprobar que el post que se quiere eliminar
    # es del usuario que hace la petición
    if post.autor != request.user:
        messages.error(request, "No eres el autor de este post.")
        return redirect("blog")

    # Existe el post y es el autor: eliminamos
    post.delete()
    messages.success(request, F"El post {post.titulo} ha sido eliminado!")
    return redirect("blog")
