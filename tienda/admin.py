from django.contrib import admin

from .models import Persona, Producto, Ruta, Distribuidor, Almacen, CompraCorporativa, Pedido, DetallePedido, DetalleCompra, MixCarga, LibroVentas, LiquidacionDistribucion, LiquidacionVentas, Kardex, DetalleFactura
# Register your models here.

admin.site.register(Persona)
admin.site.register(Producto)
admin.site.register(Ruta)
admin.site.register(Distribuidor)
admin.site.register(Almacen)
admin.site.register(CompraCorporativa)


admin.site.register(DetalleCompra)
admin.site.register(MixCarga)
admin.site.register(LibroVentas)
admin.site.register(LiquidacionDistribucion)
admin.site.register(LiquidacionVentas)
admin.site.register(Kardex)
admin.site.register(DetalleFactura)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id_pedido', 'id_cliente', 'fecha_pedido', 'total', 'estado')

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('id_detalle_pedido', 'idPedido', 'idProducto', 'cantidad', 'precioUnitario', 'subtotal')