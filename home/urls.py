from django.urls import path

from . import views

urlpatterns = [
    path('', views.MostrarProductos.as_view(), name='index'),
    path('agregar-producto/', views.add_product, name='agregar_producto'),
    # path('registrar-entrada/', views.registrar_compras, name='registrar_entrada'), Esta vista es la misma que el de las compras, no hay cambios como tal
    path('ventas/', views.ventas, name="ventas"),
    path('proveedores/', views.MostrarProveedores.as_view(), name="proveedores"),
    path("registro/proveedor", views.registrar_proveedor,
         name="registrar_proveedor"),
    path('compras/', views.MostrarCompras.as_view(), name='compras'),
    path('registro/compras/', views.registrar_compras, name='registrar_compras'),
]
