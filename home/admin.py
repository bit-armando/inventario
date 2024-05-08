from django.contrib import admin
from .models import *

models = [Proveedor, Categoria] + [Producto, Entrada, Salida, Inventario]

admin.site.register(models)
