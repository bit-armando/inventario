from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView
from django.shortcuts import render, redirect

from .models import *


clave = Producto.id_producto
precioCompra = Producto.precio_unitario
precioVenta = Producto.precio_venta
descripcion = Producto.descripcion


def index(request):
    """Ventana principal del sistema"""
    return render(request, 'VentanaPrincipal.html')


def add_product(request):
    """Vista para agregar un producto al sistema - Confirmar si se seguira usando o solo el administrador"""
    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()

    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        precio_unitario = request.POST['precio_unitario']
        precio_venta = request.POST['precio_venta']
        categoria = request.POST['categoria']
        proveedor = request.POST['proveedor']
        imagen = request.FILES['imagen']

        Producto(nombre=nombre, descripcion=descripcion,
                 precio_unitario=precio_unitario, precio_venta=precio_venta,
                 categoria=categoria, proveedor=proveedor, imagen=imagen).save()

    return render(request, 'producto.html',
                  {'categorias': categorias,
                   'proveedores': proveedores})


def registrar_compras(request):
    """Vista para registrar las compras en el sistema"""
    provedores = Proveedor.objects.all()
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()

    if request == 'POST':
        provedor = request.POST['proveedor']
        producto = request.POST['producto']
        cantidad = request.POST['cantidad']
        cantidad = request.POST['cantidad']
        fecha = request.POST['fecha']
        descripcion = request.POST['descripcion']
        # TODO guardar a la persona que hizo la entrada

        Entrada(proveedor=provedor, producto=producto,
                cantidad=cantidad, fecha=fecha, descripcion=descripcion).save()

    # TODO crear un formulario para registrar una entrada
    # TODO crear return donde redireccione a la pagina principal
    return (render(request, 'Compras.html', {
        'proveedores': provedores,
        'productos': productos,
        'categorias': categorias
    }))


class MostrarCompras(ListView):
    """Clase que desplegara las compras en la vista correspondiente"""
    model = Entrada
    template_name = 'Compras.html'
    context_object_name = 'compras'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('buscador')
        if query:
            return Entrada.objects.filter(nombre__icontains=query)
        else:
            return Entrada.objects.all()


def registrar_salida(request):
    """Vista para registrar las ventas en el sistema"""
    productos = Producto.objects.all()

    if request == 'POST':
        producto = request.POST['producto']
        cantidad = request.POST['cantidad']
        # TODO guardar solo fecha
        fecha = request.POST['fecha']
        descripcion = request.POST['descripcion']
        # TODO guardar a la persona que hizo la salida

        Salida(producto=producto, cantidad=cantidad,
               fecha=fecha, descripcion=descripcion).save()

    # TODO crear un formulario para registrar una salida
    # TODO crear return donde redireccione a la pagina principal
    return (render(request, 'Ventas.html', {
        'productos': productos
    }))

# TODO crear una vista para mostrar los productos en inventario


def proveedores(request):
    """Ventana de los proveedores del inventario"""
    return (render(request, 'Proveedores.html'))


class MostrarProveedores(ListView):
    """Clase que despliega la lista de proveedores del inventario"""
    model = Proveedor
    template_name = 'Proveedores.html'
    context_object_name = 'proveedores'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('buscador')
        if query:
            return Proveedor.objects.filter(nombre__icontains=query)
        else:
            return Proveedor.objects.all()


def registrar_proveedor(request):
    """Vista para registrar un proveedor al inventario"""
    if request.method == 'POST':
        nombre = request.POST['nombre']
        telefono = request.POST['telefono']
        correo = request.POST['email']

        telefono = str(telefono)
        Proveedor(nombre=nombre, telefono=telefono, email=correo).save()

    return redirect('proveedores')

# class MostrarProductos(ListView):
#     model = Producto
#     # template_name = 'home/productos.html'
#     context_object_name = 'productos'
#     paginate_by = 10

#     def get_queryset(self):
#         return Producto.objects.all()
