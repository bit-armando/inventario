from django.contrib import admin
from .models import *

models = [Proveedor, Categoria] + [Producto, Inventario]

admin.site.register(models)
