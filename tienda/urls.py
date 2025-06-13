from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.auth.views import LogoutView
    

#from .views import crear_transaccion_transferencia, iniciar_pago_transferencia, webhook_payku


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('nosotros', views.nosotros, name='nosotros'),
    path('contacto/', views.contacto, name='contacto'),  # Nueva ruta para contacto
    path('enviar_contacto/', views.enviar_contacto, name='enviar_contacto'),
    path('mensajes/', views.listar_mensajes, name='listar_mensajes'),

    
    path('catalogoProductos', views.catalogoProductos, name='catalogoProductos'),
    path('carrito', views.carrito_view, name='carrito'),
    path('limpiar_carrito/', views.limpiar_carrito, name='limpiar_carrito'),  # Nueva ruta para limpiar el carrito

    path('proceder_pago/', views.proceder_pago, name='proceder_pago'),
    path('confirmar_pago/', views.confirmar_pago, name='confirmar_pago'),
    
    path('agregar_al_carrito/<int:id_producto>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    
    path('lista', views.personas, name='lista'),
    
    path('lista_productos', views.lista_productos, name='lista_productos'),
    path('lista_rutas', views.lista_rutas, name='lista_rutas'),
    path('lista_distribuidores', views.lista_distribuidores, name='lista_distribuidores'),
    path('lista_almacenes', views.lista_almacenes, name='lista_almacenes'),
    path('lista_cCorporativas', views.lista_cCorporativas, name='lista_cCorporativas'),
    path('lista_pedidos', views.lista_pedidos, name='lista_pedidos'),
    path('lista_detallePedidos', views.lista_detallePedidos, name='lista_detallePedidos'),
    path('lista_detalleCompras', views.lista_detalleCompras, name='lista_detalleCompras'),
    path('lista_mixCargas', views.lista_mixCargas, name='lista_mixCargas'),
    path('lista_libroVentas', views.lista_libroVentas, name='lista_libroVentas'),
    path('lista_liquidacionDistribuidores', views.lista_lDistribuidores, name='lista_liquidacionDistribuidores'),
    path('lista_liquidacionVentas', views.lista_liquidacionVentas, name='lista_liquidacionVentas'),
    path('lista_inventarios', views.lista_inventarios, name='lista_inventarios'),
    path('lista_kardex', views.lista_kardex, name='lista_kardex'),
    path('lista_detalleFacturas', views.lista_detalleFacturas, name='lista_detalleFacturas'),
    path('lista_facturas', views.lista_facturas, name='lista_facturas'),
    path('lista_notaVentas', views.lista_notaVentas, name='lista_notaVentas'),
    
    path('login', views.login_view, name='login'),       
    
    path('lista/crear', views.crear, name='crear'),
    ##path('lista/editar',views.editar,name='editar'),
    
    path('lista_productos/crear_producto', views.crear_producto, name='crear_producto'),
    path('lista_rutas/crear_ruta', views.crear_ruta, name='crear_ruta'),
    path('lista_distribuidores/crear_distribuidor', views.crear_distribuidor, name='crear_distribuidor'),
    path('lista_almacenes/crear_almacen', views.crear_almacen, name='crear_almacen'),
    path('lista_cCorporativas/crear_cCorporativa', views.crear_cCorporativa, name='crear_cCorporativa'),
    path('lista_pedidos/crear_pedido', views.crear_pedido, name='crear_pedido'),
    path('lista_detallePedidos/crear_detallePedido', views.crear_detallePedido, name='crear_detallePedido'),
    path('lista_detalleCompras/crear_detalleCompra', views.crear_detalleCompra, name='crear_detalleCompra'),

    path('lista_mixCargas/crear_mixCarga', views.crear_mixCarga, name='crear_mixCarga'),
    path('lista_libroVentas/crear_libroVenta', views.crear_libroVenta, name='crear_libroVenta'),
    path('lista_liquidacionDistribuidores/crear_liquidacionDistribuidor', views.crear_liquidacionDistribuidor, name='crear_liquidacionDistribuidor'),
    path('lista_liquidacionVentas/crear_liquidacionVenta', views.crear_liquidacionVenta, name='crear_liquidacionVenta'),
    path('lista_inventarios/crear_inventario', views.crear_inventario, name='crear_inventario'),
    path('lista_kardex/crear_kardex', views.crear_kardex, name='crear_kardex'),
    path('lista_detalleFacturas/crear_detalleFactura', views.crear_detalleFactura, name='crear_detalleFactura'),
    path('lista_facturas/crear_factura', views.crear_factura, name='crear_factura'),
    path('lista_notaVentas/crear_notaVenta', views.crear_notaVenta, name='crear_notaVenta'),
    
    
    path('eliminar/<int:id>',views.eliminar,name='eliminar'),
    path('eliminar_producto/<int:id>',views.eliminar_producto,name='eliminar_producto'),
    path('eliminar_ruta/<int:id>',views.eliminar_ruta,name='eliminar_ruta'),
    path('eliminar_distribuidor/<int:id>',views.eliminar_distribuidor,name='eliminar_distribuidor'),
    path('eliminar_almacen/<int:id>',views.eliminar_almacen,name='eliminar_almacen'),
    path('eliminar_cCorporativa/<int:id>',views.eliminar_cCorporativa,name='eliminar_cCorporativa'),
    path('eliminar_pedido/<int:id>',views.eliminar_pedido,name='eliminar_pedido'),
    path('eliminar_detallePedido/<int:id>',views.eliminar_detallePedido,name='eliminar_detallePedido'),
    path('eliminar_detalleCompra/<int:id>',views.eliminar_detalleCompra,name='eliminar_detalleCompra'),
    path('eliminar_mixCarga/<int:id>',views.eliminar_mixCarga,name='eliminar_mixCarga'),
    path('eliminar_libroVenta/<int:id>',views.eliminar_libroVenta,name='eliminar_libroVenta'),
    path('eliminar_liquidacionDistribuidores/<int:id>',views.eliminar_liquidacionDistribuidor, name='eliminar_liquidacionDistribuidor'),
    path('eliminar_liquidacionVentas/<int:id>',views.eliminar_liquidacionVenta, name='eliminar_liquidacionVenta'),
    path('eliminar_inventario/<int:id>',views.eliminar_inventario, name='eliminar_inventario'),
    path('eliminar_kardex/<int:id>',views.eliminar_kardex, name='eliminar_kardex'),
    path('eliminar_detalleFactura/<int:id>',views.eliminar_detalleFactura, name='eliminar_detalleFactura'),
    path('eliminar_factura/<int:id>',views.eliminar_factura, name='eliminar_factura'),
    path('eliminar_notaVenta/<int:id>',views.eliminar_notaVenta, name='eliminar_notaVenta'),
    
    path('lista/editar/<int:id>',views.editar,name='editar'),

    path('lista_productos/editar_producto/<int:id>',views.editar_producto,name='editar_producto'),
    path('lista_rutas/editar_ruta/<int:id>',views.editar_ruta,name='editar_ruta'),
    path('lista_distribuidores/editar_distribuidor/<int:id>',views.editar_distribuidor,name='editar_distribuidor'),
    path('lista_almacenes/editar_almacen/<int:id>',views.editar_almacen,name='editar_almacen'),
    path('lista_cCorporativas/editar_cCorporativa/<int:id>',views.editar_cCorporativa,name='editar_cCorporativa'),
    path('lista_pedidos/editar_pedido/<int:id>',views.editar_pedido,name='editar_pedido'),
    path('lista_detallePedidos/editar_detallePedido/<int:id>',views.editar_detallePedido,name='editar_detallePedido'),
    path('lista_detalleCompras/editar_detalleCompra/<int:id>',views.editar_detalleCompra,name='editar_detalleCompra'),
    path('lista_mixCargas/editar_mixCarga/<int:id>',views.editar_mixCarga,name='editar_mixCarga'),
    path('lista_libroVentas/editar_libroVenta/<int:id>',views.editar_libroVenta,name='editar_libroVenta'),
    path('lista_liquidacionDistribuidores/editar_liquidacionDistribuidor/<int:id>',views.editar_lDistribuidor,name='editar_liquidacionDistribuidor'),
    path('lista_liquidacionVentas/editar_liquidacionVenta/<int:id>',views.editar_liquidacionVenta,name='editar_liquidacionVenta'),
    path('lista_inventarios/editar_inventario/<int:id>',views.editar_inventario,name='editar_inventario'),
    path('lista_kardex/editar_kardex/<int:id>',views.editar_kardex,name='editar_kardex'),
    path('lista_detalleFacturas/editar_detalleFactura/<int:id>',views.editar_detalleFactura,name='editar_detalleFactura'),
    path('lista_facturas/editar_factura/<int:id>',views.editar_factura,name='editar_factura'),
    path('lista_notaVentas/editar_notaVenta/<int:id>',views.editar_notaVenta,name='editar_notaVenta'),    
    
    
    path('tienda', views.tienda_view, name='tienda'),  # Asegúrate de tener esta línea
    path('menu', views.menu_view, name='menu'),
    
    path('imagenes/papa.png', views.imagen_papa, name='imagenes/papa.png'),

    path('actualizar_cantidad/<int:item_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('eliminar_del_carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),

    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    
    path('logout/', LogoutView.as_view(next_page='inicio'), name='logout'),
    
    path('descargar_factura/<int:factura_id>/', views.descargar_factura, name='descargar_factura'),

    path('agregar_detalle_compra/<int:compra_id>/', views.crear_detalleCompra, name='agregar_detalle_compra'),
          
    path('webpay/iniciar/', views.iniciar_pago, name='iniciar_pago'),
    path('webpay/retorno/', views.retorno_pago, name='retorno_pago'),
    
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)