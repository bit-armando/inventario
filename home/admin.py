from django.contrib import admin
from .models import *

models = [Tipo_empleado, Usuario, Proveedor, Categoria]

admin.site.register(models)

