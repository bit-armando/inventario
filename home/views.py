from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import logout
from datetime import date


from .models import *


@login_required
def index(request):
    """Ventana principal del sistema"""
    return render(request, 'inventario-principal.html')


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

        total = int(cantidad) * producto.precio_unitario
        Entrada(producto=producto, cantidad=int(cantidad), total=total,
                fecha=date.today(), empleado=request.user.username).save()

    except Inventario.DoesNotExist:
        Inventario.objects.create(producto=producto, cantidad=int(cantidad))
        Entrada(producto=producto, cantidad=int(cantidad), total=total,
                fecha=date.today(), empleado=str(request.user)).save()

    return redirect('compras')


def actualizar_compras(request):
    if request.method == 'POST':
        folio = request.POST['entrada-editar']
        cantidad_nueva = request.POST['cantidad-nueva']

        entrada = Entrada.objects.get(id_entrada=folio)
        producto = Producto.objects.get(
            id_producto=entrada.producto.id_producto)
        inventario_producto = Inventario.objects.get(producto=producto)

        inventario_existente = inventario_producto.cantidad
        cantidad_folio = entrada.cantidad

    if cantidad_nueva.strip() == '':
        return redirect('compras')

    try:
        cantidad_antigua = inventario_existente - cantidad_folio
        cantidad_actulizada = cantidad_antigua + int(cantidad_nueva)

        entrada.cantidad = int(cantidad_nueva)
        entrada.total = producto.precio_unitario * int(cantidad_nueva)
        entrada.save()

        inventario_producto.cantidad = cantidad_actulizada
        inventario_producto.save()

    except:
        pass

    return redirect('compras')


class MostrarCompras(LoginRequiredMixin, ListView):
    """Clase que desplegara las compras en la vista correspondiente"""
    model = Entrada
    template_name = 'Compras.html'
    context_object_name = 'Entradas'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('buscador')
        if query:
            return Entrada.objects.filter(
                Q(producto__producto__icontains=query) |
                Q(producto__descripcion__icontains=query) |
                Q(producto__id_producto__icontains=query)
            )
        else:
            return Entrada.objects.order_by('-id_entrada')

    def calcular_total(self):
        """Calcular el total de las compras"""
        total = 0
        inventario = Inventario.objects.all()
        for item in inventario:
            total += item.producto.precio_unitario * item.cantidad
        return total

    def calcular_total_individual(self, producto):
        inventario = Inventario.objects.get(producto=producto)
        total_individual = inventario.producto.precio_unitario * inventario.cantidad
        return total_individual

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_precio_unitario'] = self.calcular_total()
        context['productos'] = Producto.objects.all()
        context['inventario'] = Inventario.objects.all()
        context['compras_user'] = Entrada.objects.filter(
            empleado=self.request.user.username).order_by('-id_entrada')

        for producto in context['inventario']:
            producto.total = self.calcular_total_individual(
                producto.producto)
        return context


@login_required
def ventas(request):
    """Vista para mostrar las ventas"""
    return (render(request, "Ventas.html"))


def registrar_salida(request):
    """Vista para registrar las ventas en el sistema"""
    if request.method == 'POST':
        clave = request.POST['clave']
        cantidad = request.POST['cantidad']

    if cantidad.strip() == '' or not cantidad.isdigit():
        return redirect('ventas')

    try:
        producto = Producto.objects.get(id_producto=clave)
    except:
        return redirect('ventas')

    try:
        producto_existente = Inventario.objects.get(producto=producto)
        if producto_existente.cantidad < int(cantidad):
            messages.error(
                request, 'No hay suficiente producto en el inventario')
            return redirect('ventas')
        else:
            producto_existente.cantidad -= int(cantidad)
            producto_existente.save()

            total = int(cantidad) * producto.precio_venta
            utilidad = (producto.precio_venta -
                        producto.precio_unitario) * int(cantidad)
            Salida(producto=producto, cantidad=int(cantidad), total=total, utilidad=utilidad,
                   fecha=date.today(), empleado=str(request.user)).save()

    except Inventario.DoesNotExist:
        messages.error(request, 'El producto no existe en el inventario')
        return redirect('ventas')

    return redirect('ventas')


def actualizar_ventas(request):
    if request.method == 'POST':
        folio = request.POST['salida-editar']
        cantidad_nueva = request.POST['cantidad-nueva']

        salida = Salida.objects.get(id_salida=folio)
        producto = Producto.objects.get(
            id_producto=salida.producto.id_producto)
        inventario_producto = Inventario.objects.get(producto=producto)

        inventario_existente = inventario_producto.cantidad
        cantidad_folio = salida.cantidad

    if cantidad_nueva.strip() == '':
        return redirect('ventas')

    try:
        cantidad_antigua = inventario_existente + cantidad_folio
        cantidad_actulizada = cantidad_antigua - int(cantidad_nueva)

        salida.cantidad = int(cantidad_nueva)
        salida.total = producto.precio_venta * int(cantidad_nueva)
        salida.utilidad = (producto.precio_venta -
                           producto.precio_unitario) * int(cantidad_nueva)
        salida.save()

        inventario_producto.cantidad = cantidad_actulizada
        inventario_producto.save()

    except:
        pass

    return redirect('ventas')


class MostrarVentas(LoginRequiredMixin, ListView):
    """Clase que desplegara las compras en la vista correspondiente"""
    model = Salida
    template_name = 'Ventas.html'
    context_object_name = 'Salidas'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('buscador')
        if query:
            return Inventario.objects.filter(
                Q(producto__producto__icontains=query) |
                Q(producto__descripcion__icontains=query) |
                Q(producto__id_producto__icontains=query)
            )
        else:
            return Salida.objects.order_by('-id_salida')

    # def calcular_utilidad(self, producto, cantidad):
    #     """Para productos individuales"""
    #     inventario = Inventario.objects.get(producto=producto)
    #     cantidad_nueva = Salida.objects.get(
    #         producto=producto, cantidad=cantidad)
    #     utilidad = (inventario.producto.precio_venta -
    #                 inventario.producto.precio_unitario) * int(cantidad_nueva.cantidad)
    #     return utilidad

    def total_utilidades(self):
        """Utilidades para todo el inventario"""
        total = 0
        for producto in Salida.objects.all():
            total += (producto.utilidad)
        return total

    def calcular_total_venta(self, producto):
        """Total de venta por producto"""
        total_ventas = 0
        for venta in Salida.objects.all():
            total_ventas += venta.total

        return total_ventas

    def total_ventas(self):
        total = 0
        for producto in Salida.objects.all():
            total += (producto.total)
        return total

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos'] = Producto.objects.all()
        context['total_utilidades'] = self.total_utilidades()
        context['total_ventas'] = self.total_ventas()
        context['inventario'] = Inventario.objects.all()
        context['ventas_usuario'] = Salida.objects.filter(
            empleado=self.request.user.username
        ).order_by('-id_salida')

        # for producto in context['Salidas']:
        #     producto.utilidad = self.calcular_utilidad(
        #         producto.producto, producto.cantidad)

        return context


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


def actualizar_proveedor(request):
    """Actualizar datos de proveedores"""
    if request.method == "POST":
        id_proveedor = request.POST.get('id_proveedor')
        opcion = request.POST.get('opcion')
        valor_nuevo = request.POST.get('valor_nuevo')

        try:
            proveedor = Proveedor.objects.get(id_proveedor=id_proveedor)
            if opcion == 'nombre':
                proveedor.nombre = valor_nuevo
            elif opcion == 'telefono':
                proveedor.telefono = valor_nuevo
            elif opcion == 'email':
                proveedor.email = valor_nuevo
            proveedor.save()
        except Proveedor.DoesNotExist:
            return redirect("proveedores")

    return redirect('proveedores')


class MostrarProductos(ListView):
    model = Inventario
    template_name = 'inventario-principal.html'
    context_object_name = 'inventario'
    # paginate_by = 10

    def get_queryset(self):
        if self.request.GET.get('buscador'):
            query = self.request.GET.get('buscador')
            return Inventario.objects.filter(
                Q(producto__id_producto__icontains=query) |
                Q(producto__categoria__nombre__icontains=query)
            )
        else:
            return Inventario.objects.all()

    def calcular_total(self):
        total = 0
        for producto in Inventario.objects.all():
            total += producto.producto.precio_venta * producto.cantidad
        return total

    def calcular_total_producto(self, producto):
        inventario = Inventario.objects.get(producto=producto)
        total_producto = inventario.producto.precio_venta * inventario.cantidad
        return total_producto

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['total'] = self.calcular_total()

        for producto in context['inventario']:
            producto.total = self.calcular_total_producto(producto.producto)
        return context


def logout_view(request):
    logout(request)
    return redirect('login')
