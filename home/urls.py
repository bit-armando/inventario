from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-product/', views.add_product, name='add_product'),
    path('registrar-entrada/', views.registrar_entrada, name='registrar_entrada'),
    path('registrar-salida/', views.registar_salida, name='registrar_salida'),
    path('ventana-principal/', views.ventana_principal, name="ventana_principal"),
    path('ventas/', views.ventas, name="ventas"),
    path('proveedores/', views.proveedores, name="proveedores"),
    path('compras/', views.compras, name="compras"),
]
