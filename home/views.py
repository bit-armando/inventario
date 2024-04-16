from django.views.generic import ListView
from django.http import HttpResponse

from .models import *


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def add_user(request):
    if request == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        telefono = request.POST['telefono']
        direccion = request.POST['direccion']
        contrasena = request.POST['contrasena']
        Tipo_empleado = request.POST['tipo_empleado']
        
        Usuario(nombre=nombre, apellido=apellido, 
                telefono=telefono, direccion=direccion,
                contrasena=contrasena,
                tipo_empleado=Tipo_empleado).save()
    
    # TODO crear un formulario para agregar un usuario
    # TODO crear return donde redireccione a la pagina principal
    # TODO hashear la contraseña
    

def registrar_entrada(request):
    if request == 'POST':
        provedor = request.POST['proveedor']
        producto = request.POST['producto']
        cantidad = request.POST['cantidad']
        cantidad = request.POST['cantidad']
        #TODO guardar solo fecha
        fecha = request.POST['fecha']
        descripcion = request.POST['descripcion']
        #TODO guardar a la persona que hizo la entrada
        
        Entrada(proveedor=provedor, producto=producto, 
                cantidad=cantidad, fecha=fecha, descripcion=descripcion).save()
    
    # TODO crear un formulario para registrar una entrada
    # TODO crear return donde redireccione a la pagina principal
    
def resgistar_salida(request):
    if request == 'POST':
        producto = request.POST['producto']
        cantidad = request.POST['cantidad']
        #TODO guardar solo fecha
        fecha = request.POST['fecha']
        descripcion = request.POST['descripcion']
        #TODO guardar a la persona que hizo la salida
        
        Salida(producto=producto, cantidad=cantidad, 
               fecha=fecha, descripcion=descripcion).save()
        
    # TODO crear un formulario para registrar una salida
    # TODO crear return donde redireccione a la pagina principal
    
#TODO crear una vista para mostrar los productos en inventario


# class MostrarProductos(ListView):
#     model = Producto
#     # template_name = 'home/productos.html'
#     context_object_name = 'productos'
#     paginate_by = 10
    
#     def get_queryset(self):
#         return Producto.objects.all()