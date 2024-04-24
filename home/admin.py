from django.contrib import admin
from .models import *

models = [Tipo_empleado, Usuario, Proveedor, Categoria,
          Producto, Inventario, Categoria, Entrada, Salida]

admin.site.register(models)
