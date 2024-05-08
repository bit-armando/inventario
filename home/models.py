from django.contrib.auth.hashers import make_password
from django.db import models


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
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    # Vista Admin
    id_producto = models.CharField(primary_key=True, max_length=10)
    producto = models.CharField(max_length=50, default='')
    descripcion = models.CharField(max_length=255)
    precio_unitario = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    precio_venta = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.CASCADE, default='')
    imagen = models.ImageField(
        upload_to='productos/', default='productos/default.png')

    def __str__(self):
        return self.id_producto

    def save(self, *args, **kwargs):
        if self.imagen:
            filename = f"{self.id_producto}.{self.imagen.name.split('.')[-1]}"
            self.imagen.name = filename
        super().save(*args, **kwargs)


class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return self.producto.id_producto


class Entrada(models.Model):
    id_entrada = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha = models.DateField()
    empleado = models.CharField(default='', max_length=50)

    def __str__(self):
        return str(self.fecha)


class Salida(models.Model):
    id_salida = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField()
    empleado = models.CharField(default='', max_length=50)

    def __str__(self):
        return self.fecha
