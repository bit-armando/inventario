from django.db import models

class Proveedor(models.Model):
    id_proveedor = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return self.nombre
class Categoria(models.Model):
    id_categoria = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    


class Producto(models.Model):
    id_producto = models.CharField(primary_key=True, max_length=10)
    descripcion = models.CharField(max_length=255)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion

class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

class Entradas(models.Model):
    id_entrada = models.CharField(primary_key=True, max_length=10)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateField()
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.id_entrada

class Salida(models.Model):
    id_salida = models.CharField(primary_key=True, max_length=10)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateField()
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.id_salida