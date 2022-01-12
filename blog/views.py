from django.http import HttpResponse
from django.shortcuts import render
from .forms import FormularioPost #importamos el formulario Post

# Create your views here.

def index(request):
    #return HttpResponse("¡Hola, bienvenid@ al Blog!")
    return render(request, "blog.html")

def crear_post(request):
    form = FormularioPost()#aquí tendríamos el formulario
    return render(request, "crear_post.html", {"form": form})#y se lo pasamos a la vista crear_post.html

