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


def compras(request):
    """Ventana de compras"""
    return (render(request, "Compras.html"))


def registrar_compras(request):
    """Vista para registrar las compras en el sistema"""
    if request.method == 'POST':
        clave = request.POST['clave']
        cantidad = request.POST['cantidad']

    # En caso de que se seleccione a cerrar el formulario
    if cantidad.strip() == '' or not cantidad.isdigit():
        return redirect('compras')

    try:
        producto = Producto.objects.get(id_producto=clave)
    except Producto.DoesNotExist:
        return redirect('compras')

    try:
        inventario_existente = Inventario.objects.get(producto=producto)
        inventario_existente.cantidad += int(cantidad)
        inventario_existente.save()
    except Inventario.DoesNotExist:
        Inventario.objects.create(producto=producto, cantidad=int(cantidad))

    return redirect('compras')


class MostrarCompras(ListView):
    """Clase que desplegara las compras en la vista correspondiente"""
    model = Inventario
    template_name = 'Compras.html'
    context_object_name = 'inventario'
    paginate_by = 10

    def get_queryset(self):
        # query = self.request.GET.get('buscador')
        # if query:
        #     return Producto.objects.filter(nombre__icontains=query)
        # else:
        return Inventario.objects.all()

    def calcular_total(self):
        """Calcular el total de las compras"""
        total = 0
        inventario = Inventario.objects.all()
        for item in inventario:
            total += item.producto.precio_unitario * item.cantidad
        return total

    def calcular_total_individual(self):
        """Calcular el total individual"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_individual'] = self.calcular_total_individual()
        context['total_precio_unitario'] = self.calcular_total()
        return context


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

        if (nombre == '' or telefono == '' or correo == ''):
            return redirect('proveedores')
        else:
            Proveedor(nombre=nombre, telefono=telefono, email=correo).save()

    return redirect('proveedores')


class MostrarProductos(ListView):
    model = Inventario
    template_name = 'VentanaPrincipal.html'
    context_object_name = 'inventario'
    paginate_by = 10

    def get_queryset(self):
        return Inventario.objects.all()
