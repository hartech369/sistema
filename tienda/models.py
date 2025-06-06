from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime
from datetime import timezone
from django.forms import ValidationError
from django.utils import timezone  # Usa esta importación en lugar de datetime.timezone
from .utils import calcular_dv, calcular_subtotal  # Importa la función de cálculo
from django.db import models
# Create your models here.
from django.db import models


class PersonaManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Cifra la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Persona(AbstractBaseUser):
    id_persona = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    rut = models.CharField(max_length=8, unique=True, blank=True, null=True)
    diVerifica = models.CharField(max_length=2, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    direccion = models.TextField(blank=True, null=True)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    mapa_url = models.URLField(null=True, blank=True) 

    rol = models.CharField(max_length=50, choices=[
        ('Cliente', 'Cliente'),
        ('Vendedor', 'Vendedor'),
        ('Administrador', 'Administrador')
    ])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    password = models.CharField(max_length=128, default=make_password("contraseña_temporal"))

    objects = PersonaManager()

    USERNAME_FIELD = 'email'  # Usar el correo electrónico como nombre de usuario
    REQUIRED_FIELDS = ['nombres', 'apellidos']  # Campos requeridos al crear un usuario

    def save(self, *args, **kwargs):
        self.nombres = self.nombres.upper()
        self.apellidos = self.apellidos.upper()
        self.rut = self.rut.upper()
        self.diVerifica = self.diVerifica.upper()
        self.telefono = self.telefono.upper()
        self.direccion = self.direccion.upper()
        self.ciudad = self.ciudad.upper()
        self.rol = self.rol.upper()
        if self.rut:  # Solo calcular si hay un RUT
            self.diVerifica = calcular_dv(self.rut)  # Calcula el dígito verificador
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - RUT: {self.rut}-{self.diVerifica}"


class Ruta(models.Model):
    id_ruta = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(default='')
    zona = models.CharField(max_length=4, default='')
    
    def __str__(self):
        return self.nombre
    
class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Persona, on_delete=models.CASCADE, default=None)
    fecha_pedido = models.DateTimeField(default=timezone.now)
    fecha_entrega = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    estado = models.CharField(max_length=50, choices=[('Pendiente', 'Pendiente'), ('En proceso', 'En proceso'), ('Completado', 'Completado'), ('Cancelado', 'Cancelado')])  
    id_ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE, null=False, blank=True, default=None)

    def __str__(self):
        return f"Pedido {self.id_pedido} - {self.id_cliente.nombres}"
    
    
class CompraCorporativa(models.Model):
    id_compra_corporativa = models.AutoField(primary_key=True)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=0)  # Total monetario
    total_cantidad = models.PositiveIntegerField(default=0)     # Cantidad acumulada
    estado = models.CharField(max_length=50, default='Completado')
    numeroDocumento = models.CharField(max_length=15, default='')
    tipoDocumento = models.CharField(max_length=15, default='')

    def __str__(self):
        return f"Compra Corporativa {self.id_compra_corporativa}"


class Distribuidor(models.Model):
    id_distribuidor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=11, unique=True)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre



class Almacen(models.Model):
    id_almacen = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    ubicacion = models.TextField()
    capacidad = models.IntegerField(default=0)
    estado = models.CharField(max_length=50, default='Activo')

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.IntegerField()
    categoria = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='productos/', verbose_name="producto", null=True)
    id_almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, null=True)  # ✅ Relación completa
    
    def __str__(self):
        return self.nombre + self.descripcion
    
    def delete(self, using=None, keep_parents=False):
        self.imagen.storage.delete(self.imagen.name)
        super().delete()

class DetalleCompra(models.Model):
    id_detalle_compra = models.AutoField(primary_key=True)
    id_compraCorporativa = models.ForeignKey(CompraCorporativa, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precioUnitario = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    descuento = models.DecimalField(max_digits=10, decimal_places=0, default=0) 
    subtotal = models.DecimalField(max_digits=10, decimal_places=0)
    numeroDoc= models.CharField(max_length=15, default='')
    
    '''
    def save(self, *args, **kwargs):
        # Calcula el subtotal automáticamente antes de guardar
        self.subtotal = calcular_subtotal(self.cantidad, self.precioUnitario, self.descuento)

        # Si es nueva compra, actualizar stock y kardex
        if not self.pk:
            self.id_producto.stock += self.cantidad
            self.id_producto.save()
            
            Kardex.objects.create(
                producto=self.id_producto,
                tipo_movimiento='Entrada',
                cantidad=self.cantidad,
                stockFinal=self.id_producto.stock,
                idAlmacen=self.id_producto.id_almacen  # Asegúrate de tener esta relación
            )
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Detalle Compra {self.id_detalle_compra}"
    '''
    def save(self, *args, **kwargs):
        # Calcula subtotal
        self.subtotal = calcular_subtotal(self.cantidad, self.precioUnitario, self.descuento)

        # Obtiene la compra corporativa relacionada
        compra = self.id_compraCorporativa
        producto = self.id_producto

        if not self.pk:
            # NUEVO: Actualiza stock, kardex y campos de CompraCorporativa
            producto.stock += self.cantidad
            producto.save()

            compra.total += self.subtotal
            compra.total_cantidad += self.cantidad
            compra.numeroDocumento = self.numeroDoc  # Asigna el número de documento
            compra.save(update_fields=['total', 'total_cantidad', 'numeroDocumento'])

            Kardex.objects.create(
                producto=producto,
                tipo_movimiento='Entrada',
                cantidad=self.cantidad,
                stockFinal=producto.stock,
                idAlmacen=producto.id_almacen
            )
        else:
            # ACTUALIZADO: Compara valores anteriores
            original = DetalleCompra.objects.get(pk=self.pk)

            if original.numeroDoc != self.numeroDoc:
                raise ValidationError("No se puede modificar el número de documento.")

            diferencia_cantidad = self.cantidad - original.cantidad
            diferencia_total = self.subtotal - original.subtotal

            producto.stock += diferencia_cantidad
            producto.save()

            compra.total += diferencia_total
            compra.total_cantidad += diferencia_cantidad
            compra.save(update_fields=['total', 'total_cantidad'])

        super().save(*args, **kwargs)    

class MixCarga(models.Model):
    id_mix_carga = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    descripcion = models.TextField(default='')
    cantidad = models.PositiveIntegerField()
    id_distribuidor = models.ForeignKey(Distribuidor, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"Mix Carga {self.id_mix_carga}"


class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    numeroFactura= models.CharField(max_length=50, default='')
    fechaEmision = models.DateTimeField(auto_now_add=True)
    totalBruto = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    
    estado= models.CharField(max_length=50, default='Completado')
    tipoDocumento= models.CharField(max_length=50, default='Factura')
    
    idPedido= models.ForeignKey(Pedido, on_delete=models.CASCADE, null=True)
    #idMixCarga = models.ForeignKey(MixCarga, on_delete=models.SET_NULL, null=True)

    razon_social = models.CharField(max_length=200, default='')
    direccion_fiscal = models.TextField(default='')
    rut = models.CharField(max_length=11, default= '')    

    def __str__(self):
        return f"Factura {self.id_factura}"

class NotaVenta(models.Model):
    id_nota_venta = models.AutoField(primary_key=True)
    fecha_emision = models.DateTimeField(default=timezone.now)
    totalBruto = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    estado = models.CharField(max_length=50, default='Completado')
    id_factura = models.ForeignKey(Factura, on_delete=models.CASCADE, null=True, blank=True)  # Una nota de venta pertenece a una factura
        
    def __str__(self):
        return f"Nota de Venta {self.id_nota_venta}"


class LibroVentas(models.Model):
    id_libro_ventas = models.AutoField(primary_key=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    total_Facturado = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    
    id_factura = models.ForeignKey(Factura, on_delete=models.CASCADE, null=True)  # Un libro de ventas contiene múltiples facturas
    
    def __str__(self):
        return f"Libro Ventas {self.id_libro_ventas}"


class LiquidacionDistribucion(models.Model):
    id_liquidacion_distribucion = models.AutoField(primary_key=True)
    distribuidor = models.ForeignKey(Distribuidor, on_delete=models.CASCADE)
    fecha_liquidacion = models.DateTimeField(default=timezone.now)
    total_distribuido = models.DecimalField(max_digits=10, decimal_places=0)
    comision = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    estado = models.CharField(max_length=50, default='Pendiente')
    idMixCarga = models.ForeignKey(MixCarga, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"Liquidación Distribución {self.id_liquidacion_distribucion}"


class LiquidacionVentas(models.Model):
    id_liquidacion_ventas = models.AutoField(primary_key=True)
    fecha_liquidacion = models.DateTimeField(default=timezone.now)
    total_liquidado = models.DecimalField(max_digits=10, decimal_places=0)
    cantidadVentas = models.IntegerField(default=0)
    idMixCarga = models.ForeignKey(MixCarga, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Liquidación Ventas {self.id_liquidacion_ventas}"



class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(default=timezone.now)
    stockDisponible = models.PositiveIntegerField(default=1)
    stockReservado = models.PositiveIntegerField(default=1)
    ultimaActualizacion =  models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Inventario {self.id_inventario}"
    
class Kardex(models.Model):
    id_kardex = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_movimiento = models.DateTimeField(default=timezone.now)
    tipo_movimiento = models.CharField(max_length=50, choices=[('Entrada', 'Entrada'), ('Salida', 'Salida')])
    cantidad = models.PositiveIntegerField(default=0)
    stockFinal = models.PositiveIntegerField(default=0)
    idMixCarga = models.ForeignKey(MixCarga, on_delete=models.CASCADE, null=True)
    idAlmacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, null=True) 
    idInventario = models.ForeignKey(Inventario, on_delete=models.CASCADE, null=True)
    idDetalleCompra= models.ForeignKey(DetalleCompra, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"Kardex {self.id_kardex}"
    

class DetallePedido(models.Model):
    id_detalle_pedido = models.AutoField(primary_key=True)
    idPedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precioUnitario= models.DecimalField(max_digits=10, decimal_places=0, default=0)
    descuento= models.DecimalField(max_digits=10, decimal_places=0, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=0)

    def save(self, *args, **kwargs):
        # Calcula el subtotal automáticamente antes de guardar
        self.subtotal = calcular_subtotal(self.cantidad, self.precioUnitario, self.descuento)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Detalle {self.id_detalle_pedido} - Pedido {self.idPedido.id_pedido}"

class DetalleFactura(models.Model):
    id_detalle_factura = models.AutoField(primary_key=True)
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)  # ✅ Relación con Producto
    cantidad= models.PositiveIntegerField()
    precioUnitario= models.DecimalField(max_digits=10, decimal_places=0, default=0)
    descuento=models.DecimalField(max_digits=10, decimal_places=0, default=0)
    impuestoAplicado= models.CharField(max_length=50, default='')
    subtotal= models.DecimalField(max_digits=10, decimal_places=0, default=0) 
    id_factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        # Calcula el subtotal automáticamente antes de guardar
        self.subtotal = calcular_subtotal(
            self.cantidad, 
            self.precioUnitario, 
            self.descuento,
            self.impuestoAplicado
        )
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Detalle Factura {self.id_detalle_factura}"

