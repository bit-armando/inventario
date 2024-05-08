from django.contrib import admin
from .models import *

models = [Folio, FolioProducto, Proveedor, Categoria] + [Producto, Entrada, Salida, Inventario]

admin.site.register(models)
