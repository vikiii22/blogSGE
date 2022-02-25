from django.db import models
from django.contrib.auth.models import User
import os


# Create your models here.

# creamos una clase que extiende de models
class Categoria(models.Model):
    # definimos el tipo y sus atributos
    # NO tenemos clave primaria - PK, la asigna django
    # CharField (input text), TextField (textarea)...
    # atributos: long max 100, no permite nulos, campo único
    # verbose_name: nombre de la etiqueta del formulario
    nombre = models.CharField(max_length=100, null=False, unique=True, verbose_name='Nombre')

    # str nos permite devolver la información de la clase en forma de cadena
    def __str__(self):
        # si hacemos un print, en vez de mostrar el objeto, nos mostrará el nombre de la Categoría
        return self.nombre
        # return "Categoría con id %d y nombre %s" % (self.id, self.nombre)

    # Meta nos permite cambiar el comportamiento de las migraciones en BBDD
    # auth_user se llama así porque pertenece a la aplicación auth y el modelo user
    # por esa regla, categorías se llamaría por defecto: blog_Categoria
    # con Meta cambiamos este comportamiento
    class Meta:
        db_table = 'categories'
        verbose_name = 'Categoría'  # nombre administración
        verbose_name_plural = 'Categorías'
        ordering = ['id']  # ordenación ascendente -- [-id] ordenación descendente


class Product(models.Model):
    # on_delete=CASCADE si se elimina el usuario se eliminan sus posts
    # null a True y blank a True permite valores nulos por consistencia de BBDD
    # de esta manera cuando se crea el registro de post en BBDD, como todavía no hemos asignado el usuario, vamos a guardarlo sin hacer el commit; pudiendo crear la instancia,
    # y sin establecer los cambios persistentes en BBDD vamos a poder establecer el usuario para realizar el commit con todos los cambios
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100, unique=True, null=False, verbose_name='Título')
    contenido = models.TextField(null=True, verbose_name='Contenido del post')
    # nos hace falta la dependencia Pillow - instalalá
    imagen = models.ImageField(upload_to='posts/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen del post')
    # fecha de alta del post para llevar el registro
    # auto_now_add se define automáticamente con la fecha de inserción
    # verbose_name no se verá porque no es un campo que mostraremos en el formulario... se puede quitar
    precio = models.FloatField(null=True, default=1)
    fecha_alta = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de alta')
    fecha_actualizacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de actualización')

    def __str__(self):
        return self.titulo

        # sobreescribiendo un método - instancia (self) y argumentos (*args, **kwargs) de un método

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.imagen.path):  # si el archivo existe
            os.remove(self.imagen.path)  # se elimina del sistemas de archivo
        super(Product, self).delete(*args, **kwargs)  # borrado del post llamando al constructor

    # podríamos sobreescribir todos los métodos disponibles - save, update...

    class Meta:
        db_table = 'products'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']
