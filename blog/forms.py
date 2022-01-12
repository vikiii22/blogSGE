from django import forms #importamos los formularios
from .models import Post # y el modelo de Post


class FormularioPost(forms.ModelForm): #extiende el modelo form
    class Meta:
        #creación de formulario con apariencia bootstrap y validado
        model = Post #modelo con el que va a trabajar
        fields = ('categoria', 'titulo', 'contenido', 'imagen')# campos a mostrar
        #no se han de decir los tipos porque esto ya lo hicimos cuando generamos el modelo