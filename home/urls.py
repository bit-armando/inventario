from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('agregar-producto/', views.add_product, name='agregar_producto'),
    path('registrar-entrada/', views.registrar_entrada, name='registrar_entrada'),
    path('principal/', views.ventana_principal, name='ventana_principal'),
    path('ventas/', views.ventas, name="ventas"),
    path('proveedores/', views.proveedores, name="proveedores"),
    path('compras/', views.compras, name='compras'),
]
