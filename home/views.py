from django.views.generic import ListView
from django.shortcuts import render

from .models import *


clave = Producto.id_producto
precioCompra = Producto.precio_unitario
precioVenta = Producto.precio_venta
descripcion = Producto.descripcion


def index(request):
    return render(request, 'iniciarSesion.html')


def add_product(request):
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
    

def registrar_entrada(request):
    provedores = Proveedor.objects.all()
    productos = Producto.objects.all()
    
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
    
def resgistar_salida(request):
    productos = Producto.objects.all()
    
    if request == 'POST':
        producto = request.POST['producto']
        cantidad = request.POST['cantidad']
        #TODO guardar solo fecha
        fecha = request.POST['fecha']
        descripcion = request.POST['descripcion']
        # TODO guardar a la persona que hizo la salida

        Salida(producto=producto, cantidad=cantidad,
               fecha=fecha, descripcion=descripcion).save()

    # TODO crear un formulario para registrar una salida
    # TODO crear return donde redireccione a la pagina principal
    
#TODO crear una vista para mostrar los productos en inventario


def ventana_principal(request):
    return (render(request, 'VentanaPrincipal.html'))

# class MostrarProductos(ListView):
#     model = Producto
#     # template_name = 'home/productos.html'
#     context_object_name = 'productos'
#     paginate_by = 10

#     def get_queryset(self):
#         return Producto.objects.all()
