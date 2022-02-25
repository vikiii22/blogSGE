from django.contrib import admin
from .models import Categoria, Product

# Register your models here.
admin.site.register([Categoria, Product])