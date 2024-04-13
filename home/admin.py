from django.contrib import admin
from .models import *

models = [Proveedor, Categoria, Producto, Inventario, Entrada, Salida]

admin.site.register(models)

