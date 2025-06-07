from django import forms
from .models import DetalleFactura, Factura, Persona, Producto, Ruta, Distribuidor, Almacen, CompraCorporativa, Pedido, DetallePedido, DetalleCompra, MixCarga, LibroVentas, LiquidacionDistribucion, LiquidacionVentas, Inventario, Kardex, NotaVenta, MensajeContacto
from django.contrib.auth.forms import PasswordChangeForm



class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = [
            'nombres', 'apellidos', 'rut', 'diVerifica',
            'telefono', 'email', 'direccion', 'ciudad',
            'mapa_url', 'rol'
        ]
        
        
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        
class RutaForm(forms.ModelForm):
    class Meta:
        model = Ruta
        fields = '__all__'
        

class DistribuidorForm(forms.ModelForm):
    class Meta:
        model = Distribuidor
        fields = '__all__'
        
        
class AlmacenForm(forms.ModelForm):
    class Meta:
        model = Almacen
        fields = '__all__'
        
        
class CCorporativaForm(forms.ModelForm):
    class Meta:
        model = CompraCorporativa
        fields = '__all__'
        

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        widgets = {
            'fecha_pedido': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_entrega': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
        fields = '__all__'
              
class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = '__all__'
        
class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = '__all__'

class MixCargaForm(forms.ModelForm):
    class Meta:
        model = MixCarga
        fields = '__all__'
        

class LibroVentasForm(forms.ModelForm):
    class Meta:
        model = LibroVentas
        widgets = {
            'fecha_registro': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        fields = '__all__'
        


class LiquidacionDistribucionForm(forms.ModelForm):
    class Meta:
        model = LiquidacionDistribucion
        widgets = {
            'fecha_liquidacion': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
      
        fields = '__all__'
        
        
class LiquidacionVentasForm(forms.ModelForm):
    class Meta:
        model = LiquidacionVentas
        widgets = {
            'fecha_liquidacion': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
       
        fields = '__all__'



class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['fecha', 'stockDisponible', 'stockReservado', 'ultimaActualizacion']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'ultimaActualizacion': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
        
class KardexForm(forms.ModelForm):
    class Meta:
        model = Kardex
        widgets = {
            'fecha_movimiento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        fields = '__all__'
        
class DetalleFacturaForm(forms.ModelForm):
    class Meta:
        model = DetalleFactura
        fields = '__all__'
        
        
class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        widgets = {
            'fechaEmision': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        fields = '__all__'



class NotaVentaForm(forms.ModelForm):
    class Meta:
        model = NotaVenta
        widgets = {
            'fecha_emision': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        fields = '__all__'
        
class MensajeContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'mensaje']

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombres', 'apellidos', 'telefono', 'direccion', 'email', 'ciudad', 'mapa_url']        
