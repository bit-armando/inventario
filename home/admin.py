from django.contrib import admin
from .models import *

models = [Tipo_Empleado, Usuario, Proveedor, Categoria]

admin.site.register(models)
