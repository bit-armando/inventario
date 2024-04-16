from django.db import models

class Tipo_empleado(models.Model):
    #TODO Dejar en vista admin
    id_empleado = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50)
    
    def __str__(self):
        return self.tipo
    
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    direccion = models.CharField(max_length=255)
    contrasena = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    tipo_empleado = models.ForeignKey(Tipo_empleado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + " " + self.apellido
    
    
class Proveedor(models.Model):
    # TODO Dejar en vista admin
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return self.nombre
    
    
class Categoria(models.Model):
    # TODO Dejar en vista admin
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    

class Producto(models.Model):
    #TODO Dejar en vista admin
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, default='')
    descripcion = models.CharField(max_length=255)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    #TODO agregar precio venta
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, default='')
    #TODO agregar imagen

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
    fecha = models.DateField()
    descripcion = models.CharField(max_length=255)
    empleado = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.fecha
    

class Salida(models.Model):
    id_salida = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateField()
    descripcion = models.CharField(max_length=255)
    empleado = models.ForeignKey(Usuario, on_delete=models.CASCADE, default='')

    def __str__(self):
        return self.fecha