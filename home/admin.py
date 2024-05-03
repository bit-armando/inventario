from django.contrib import admin
from .models import *

models = [Tipo_Empleado, Usuario, Proveedor, Categoria] + [Producto, Entrada, Salida, Inventario]

admin.site.register(models)
