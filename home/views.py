from django.views.generic import ListView
from django.shortcuts import render, redirect

from .models import *


def index(request):
    return render(request, 'VentanaPrincipal.html')


def add_product(request):
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

        Producto(id_producto=clave, descripcion=descripcion,
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
    return(render(request, 'Compras.html',{
        'proveedores': provedores,
        'productos': productos
    }))


def resgistar_salida(request):
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
    return(render(request, 'Ventas.html', {
        'productos': productos
    }))


class MostrarProveedores(ListView):
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
