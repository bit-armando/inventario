from django.contrib import admin
from .models import *

models = [Tipo_empleado, Usuario, Proveedor, Categoria,
          Producto, Inventario, Entrada, Salida]

admin.site.register(models)
