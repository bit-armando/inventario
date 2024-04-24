from django.contrib.auth.hashers import make_password
from django.db import models


class Tipo_Empleado(models.Model):
    # Vista Admin
    id_empleado = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tipo


class Usuario(models.Model):
    # Vista Admin
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    direccion = models.CharField(max_length=255)
    contrasena = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    tipo_empleado = models.ForeignKey(Tipo_Empleado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + " " + self.apellido

    def save(self, *args, **kwargs):
        self.contrasena = make_password(self.contrasena)
        super().save(*args, **kwargs)

class Proveedor(models.Model):
    # Vista Admin
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    # Vista Admin
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    # Vista Admin
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, default='')
    descripcion = models.CharField(max_length=255)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, default='')
    imagen = models.ImageField(upload_to='productos/', default='productos/default.jpg')

    def __str__(self):
        return self.nombre


class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return self.producto.descripcion


class Entrada(models.Model):
    id_entrada = models.AutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField()
    descripcion = models.CharField(max_length=255)
    empleado = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.fecha


class Salida(models.Model):
    id_salida = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField()
    descripcion = models.CharField(max_length=255)
    empleado = models.ForeignKey(Usuario, on_delete=models.CASCADE, default='')

    def __str__(self):
        return self.fecha