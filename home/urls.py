from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('agregar-producto/', views.add_product, name='agregar_producto'),
    path('registrar-entrada/', views.registrar_entrada, name='registrar_entrada'),
    path('ventas/', views.resgistar_salida, name="ventas"),
    path('proveedores/', views.MostrarProveedores.as_view(), name="proveedores"),
    path("registro/proveedor", views.registrar_proveedor, name="registrar_proveedor"),
    path('compras/', views.registrar_entrada, name='compras'),
]
