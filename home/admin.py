from django.contrib import admin
from .models import *

models = [Proveedor, Categoria, Producto, Inventario, Entradas, Salida]

admin.site.register(models)

