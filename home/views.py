from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView
from django.shortcuts import render, redirect

from .models import *


def index(request):
    """Ventana principal del sistema"""
    return render(request, 'VentanaPrincipal.html')


def add_product(request):
    """Vista para agregar un producto al sistema - Confirmar si se seguira usando o solo el administrador"""
    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()

    if request.method == 'POST':
        clave = request.POST['clave']
        descripcion = request.POST['descripcion']
        precio_unitario = request.POST['precio_unitario']
        precio_venta = request.POST['precio_venta']
        categoria = request.POST['categoria']
        proveedor = request.POST['proveedor']
        imagen = request.FILES['imagen']

        Entrada(id_entrada=clave, descripcion=descripcion,
                precio_unitario=precio_unitario, precio_venta=precio_venta,
                categoria=categoria, proveedor=proveedor, imagen=imagen).save()

    return render(request, 'producto.html',
                  {'categorias': categorias,
                   'proveedores': proveedores})


def registrar_compras(request):
    """Vista para registrar las compras en el sistema"""
    proveedores = Proveedor.objects.all()
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        id_proveedor = request.POST.get('proveedor')
        id_producto = request.POST.get('producto')
        cantidad = request.POST.get('cantidad')
        precio_unitario = request.POST.get('precio_unitario')
        precio_venta = request.POST.get('precio_venta')
        fecha = request.POST.get('fecha')
        descripcion = request.POST.get('descripcion')

        proveedor = Proveedor.objects.get(pk=id_proveedor)
        producto = Producto.objects.get(pk=id_producto)

        # Actualizar el precio unitario y de venta del producto si es necesario
        if precio_unitario:
            producto.precio_unitario = precio_unitario
        if precio_venta:
            producto.precio_venta = precio_venta
        producto.save()

        nueva_entrada = Entrada(
            proveedor=proveedor,
            producto=producto,
            cantidad=cantidad,
            fecha=fecha,
            descripcion=descripcion,
        )
        nueva_entrada.save()

    return render(request, 'Compras.html', {
        'proveedores': proveedores,
        'productos': productos,
        'categorias': categorias,
    })


class MostrarCompras(ListView):
    """Clase que desplegara las compras en la vista correspondiente"""
    model = Entrada
    template_name = 'Compras.html'
    context_object_name = 'entradas'
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
