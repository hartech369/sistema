import logging
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from django.conf import settings


from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.forms import ValidationError
from django.test import TransactionTestCase
from django.utils import timezone
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib import admin
#from weasyprint import HTML
from django.template.loader import render_to_string

from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter, inch
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from tienda.utils import calcular_subtotal, numero_a_palabras


from .forms import DetalleFacturaForm, FacturaForm, KardexForm, NotaVentaForm, PersonaForm, ProductoForm, RutaForm, DistribuidorForm, AlmacenForm, CCorporativaForm, PedidoForm, DetallePedidoForm, DetalleCompraForm, MixCargaForm, LibroVentasForm, LiquidacionDistribucionForm, LiquidacionVentasForm, InventarioForm, MensajeContactoForm, PerfilForm
from .models import DetalleFactura, Factura, Inventario, Kardex, NotaVenta, Persona, Producto, Ruta, Distribuidor, Almacen, CompraCorporativa, Pedido, DetallePedido, DetalleCompra, MixCarga, LibroVentas, LiquidacionDistribucion, LiquidacionVentas, MensajeContacto

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage

import requests
from django.conf import settings
from django.http import JsonResponse

import uuid

from django.views.decorators.csrf import csrf_exempt
import json

from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.
def inicio(request):
    return render(request, "paginas/inicio.html")

def nosotros(request):
    return render(request, "paginas/nosotros.html")

def catalogoProductos(request):
    productos=Producto.objects.all()
    return render(request, "paginas/catalogoProductos.html", {'productos': productos})


# views.py
'''def agregar_al_carrito(request, id_producto):
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        producto = Producto.objects.get(id_producto=id_producto)
        carrito = request.session.get('carrito', {})
        if str(id_producto) in carrito:
            carrito[str(id_producto)]['cantidad'] += cantidad
        else:
            carrito[str(id_producto)] = {
                'nombre': producto.nombre,
                'precio': float(producto.precio),
                'cantidad': cantidad
            }
        request.session['carrito'] = carrito
    return redirect('carrito')'''
    
    
def agregar_detalle_compra(request, compra_id):
    compra = get_object_or_404(CompraCorporativa, id_compra_corporativa=compra_id)
    
    if request.method == 'POST':
        formulario = DetalleCompraForm(request.POST)
        if formulario.is_valid():
            detalle = formulario.save(commit=False)
            detalle.id_compraCorporativa = compra
            detalle.save()
            return redirect('agregar_detalle_compra', compra_id=compra_id)
    else:
        formulario = DetalleCompraForm()
    
    return render(request, 'detalle_compra/agregar_detalle_compra.html', {
        'formulario': formulario,
        'compra': compra
    })
    

def agregar_al_carrito(request, id_producto):
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        producto = Producto.objects.get(id_producto=id_producto)
        # Obtener el carrito de la sesión
        carrito = request.session.get('carrito', {})
        # Agregar o actualizar el producto en el carrito
        if str(id_producto) in carrito:
            carrito[str(id_producto)]['cantidad'] += cantidad
        else:
            carrito[str(id_producto)] = {
                'nombre': producto.nombre,
                'precio': float(producto.precio),
                'cantidad': cantidad,
            }
        # Guardar el carrito en la sesión
        request.session['carrito'] = carrito
        request.session.modified = True  # ✅ Asegura que la sesión se guarde

    return redirect('carrito')


def carrito_view(request):
    # Obtener el carrito de la sesión
    carrito = request.session.get('carrito', {})

    for item_id, item_data in carrito.items():
    # Calcular subtotales y total
        precio = float(item_data['precio'])
        cantidad = int(item_data['cantidad'])
        item_data['subtotal'] = precio * cantidad

    total = sum(item_data['subtotal'] for item_data in carrito.values())
    request.session.modified = True  # ✅ Marca la sesión como modificada
    request.session['carrito'] = carrito
    return render(request, 'paginas/carrito.html', {'carrito': carrito, 'total': total})


'''def carrito_view(request):
    carrito = request.session.get('carrito', {})
    for item_id, item_data in carrito.items():
        precio = item_data['precio']
        cantidad = item_data['cantidad']
        item_data['subtotal'] = precio * cantidad
    total = sum(item_data['subtotal'] for item_data in carrito.values())
    return render(request, 'paginas/carrito.html', {'carrito': carrito, 'total': total})'''
#return render(request, 'paginas/carrito.html', {'carrito': carrito, 'subtotal': subtotal, 'total': total})

# views.py
def registrar_usuario(request):
    if request.method == 'POST':
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        email = request.POST.get('email')
        password = request.POST.get('password')
        rut = request.POST.get('rut')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        ciudad = request.POST.get('ciudad')
        mapa_url = request.POST.get('mapa_url')
        
        # Cifrar la contraseña antes de guardarla
        hashed_password = make_password(password)

        Persona.objects.create(
            nombres=nombres,
            apellidos=apellidos,
            email=email,
            password=hashed_password,
            rut=rut,
            telefono=telefono,
            direccion=direccion,
            ciudad=ciudad,
            mapa_url=mapa_url,
            
            rol='Cliente'
        )
        return redirect('login')  # Redirige al formulario de inicio de sesión
    return render(request, 'paginas/registrar_usuario.html')
    
def limpiar_carrito(request):
    # Eliminar el carrito de la sesión
    if 'carrito' in request.session:
        del request.session['carrito']
    return redirect('carrito')

'''
def proceder_pago(request):
    if request.method == 'POST':
        # Procesar el formulario de pago aquí
        return redirect('confirmar_pago')
    return render(request, 'paginas/proceder_pago.html', {'carrito': carrito})
'''

def proceder_pago(request):
    # Obtener el carrito de la sesión
    carrito = request.session.get('carrito', {})
    
    if not carrito:
        messages.error(request, "Tu carrito está vacío. Agrega productos antes de proceder al pago.")
        return redirect('catalogoProductos')
    
    # Calcular el total del carrito
    total = sum(item_data['precio'] * item_data['cantidad'] for item_data in carrito.values())
    
    if request.method == 'POST':
        # Procesar el formulario de pago aquí
        return redirect('confirmar_pago')
    
    return render(request, 'paginas/proceder_pago.html', {'carrito': carrito, 'total': total})


'''
@login_required
def confirmar_pago(request):
    if request.method == 'POST':
        # Obtener el carrito de la sesión
        carrito = request.session.get('carrito', {})
        if not carrito:
            return redirect('carrito')  # Redirigir si el carrito está vacío

        # Obtener una ruta predeterminada (puedes ajustar la lógica según tus necesidades)
        ruta_predeterminada = Ruta.objects.first()
        if not ruta_predeterminada:
            return HttpResponse("No hay rutas disponibles. Contacte al administrador.")

        # Crear un nuevo Pedido con total inicial en 0
        cliente = Persona.objects.get(id_persona=request.user.id_persona)  # Aquí deberías obtener el cliente autenticado
        pedido = Pedido.objects.create(
            id_cliente=cliente,
            fecha_pedido=timezone.now(),
            fecha_entrega=timezone.now(),
            total=0,  # Se actualizará después de agregar los detalles
            estado='Pendiente',
            id_ruta=ruta_predeterminada  # Ruta asignada por defecto
        )

        # Calcular el total del pedido
        total_pedido = 0
        for item_id, item_data in carrito.items():
            producto = Producto.objects.get(id_producto=item_id)
            cantidad = item_data['cantidad']
            precio_unitario = float(producto.precio)
            subtotal = cantidad * precio_unitario

            # Crear un DetallePedido para cada ítem en el carrito
            detalle = DetallePedido.objects.create(
                idPedido=pedido,
                idProducto=producto,
                cantidad=cantidad,
                precioUnitario=precio_unitario,
                descuento=0,  # Puedes ajustar esto si hay descuentos
                subtotal=subtotal
            )
            total_pedido += subtotal

        # Actualizar el total del pedido
        pedido.total = total_pedido
        pedido.save()

        # Limpiar el carrito después de confirmar el pago
        limpiar_carrito(request)

        return redirect('carrito')  # Redirigir al carrito o página de éxito
    return redirect('proceder_pago')
'''

@login_required
def confirmar_pago(request):
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        
        # Validar que el carrito no esté vacío
        if not carrito:
            messages.error(request, "Tu carrito está vacío")
            return redirect('carrito')

        # Obtener ruta predeterminada    
        ruta_predeterminada = Ruta.objects.first()
        cliente = Persona.objects.get(id_persona=request.user.id_persona)
                    
        # 1. Crear Pedido
        pedido = Pedido.objects.create(
            id_cliente=cliente,
            fecha_pedido=timezone.now(),
            fecha_entrega=timezone.now(),
            total=0,
            estado='Completado',
            id_ruta=ruta_predeterminada
        )

        total_pedido = 0
        detalles_pedido = []

        # 2. Procesar items del carrito y crear DetallePedido
        for item_id, item_data in carrito.items():
            producto = Producto.objects.get(id_producto=item_id)
            cantidad = item_data['cantidad']
            precio_unitario = float(producto.precio)
            subtotal = cantidad*precio_unitario
                
            # Crear detalle del pedido
            detalle = DetallePedido.objects.create(
                idPedido=pedido,
                idProducto=producto,
                cantidad=cantidad,
                precioUnitario=precio_unitario,
                descuento=0,
                subtotal=subtotal
            )
            detalles_pedido.append(detalle)
            total_pedido += subtotal

            # Actualizar total del pedido
            pedido.total = total_pedido
            pedido.save()

            # 3. Crear Factura
            factura = Factura.objects.create(
                numeroFactura=f"FACT-{pedido.id_pedido}",
                totalBruto=total_pedido,
                #iva=total_pedido * 0.19,
                
                idPedido=pedido,
                estado='Completado',
                razon_social=f"{cliente.nombres} {cliente.apellidos}",
                rut=cliente.rut,
                direccion_fiscal=cliente.direccion
            )

            # 4. Crear Detalles de Factura
            for detalle_pedido in detalles_pedido:
                DetalleFactura.objects.create(
                    idProducto = detalle_pedido.idProducto,  # ✅ Ahora sí existe
                    cantidad = detalle_pedido.cantidad,
                    precioUnitario = detalle_pedido.precioUnitario,
                    #descuento = detalle_pedido.descuento,
                    impuestoAplicado = "IVA 19%",
                    subtotal = detalle_pedido.subtotal,
                    id_factura = factura
                )

            # 5. Crear NotaVenta vinculada a la Factura
            nota_venta = NotaVenta.objects.create(
                totalBruto=total_pedido,
                #iva=total_pedido * 0.19,
                #totalNeto=total_pedido * 1.19,
                estado='Completado',
                id_factura=factura  # Relación corregida
            )

            # 6. Crear Libro de Ventas
            LibroVentas.objects.create(
                total_Facturado=factura.totalBruto,
                #total_iva=factura.iva,
                #total_Neto=factura.totalBruto
            )

            # 7. Actualizar inventario y crear Kardex
            for detalle_pedido in detalles_pedido:
                producto = detalle_pedido.idProducto
                cantidad = detalle_pedido.cantidad
                
                # Validar stock suficiente
                if producto.stock < cantidad:
                    raise ValueError(f"Stock insuficiente para {producto.nombre}")
                
                # Actualizar stock del producto
                producto.stock -= cantidad
                producto.save()

                # Crear registro en Kardex
                Kardex.objects.create(
                    producto=producto,
                    fecha_movimiento=timezone.now(),
                    tipo_movimiento='Salida',
                    cantidad=cantidad,
                    stockFinal=producto.stock,
                    idAlmacen=Almacen.objects.first()  # Asumiendo que Ruta representa Almacén
                )

        # Limpiar carrito
        limpiar_carrito(request)
        
        
        # Redirigir a página de éxito
        return render(request, 'paginas/pago_exitoso.html', {
            'pedido': pedido,
            'factura': factura,
            'nota_venta': nota_venta
        })

    
    return redirect('proceder_pago')

@login_required
def lista_productos(request):
    productos=Producto.objects.all()
    return render(request, "lista_productos/index_producto.html", {'productos': productos})
    
@login_required
def lista_rutas(request):
    rutas=Ruta.objects.all()
    return render(request, "lista_rutas/index_ruta.html", {'rutas': rutas})


@login_required
def lista_distribuidores(request):
    distribuidores=Distribuidor.objects.all()
    return render(request, "lista_distribuidores/index_distribuidor.html", {'distribuidores': distribuidores})


@login_required
def lista_almacenes(request):
    almacenes=Almacen.objects.all()
    return render(request, "lista_almacenes/index_almacen.html", {'almacenes': almacenes})

@login_required
def lista_cCorporativas(request):
    cCorporativas=CompraCorporativa.objects.all()
    return render(request, "lista_cCorporativas/index_cCorporativa.html", {'cCorporativas': cCorporativas})

@login_required
def lista_pedidos(request):
    pedidos=Pedido.objects.all()
    return render(request, "lista_pedidos/index_pedido.html", {'pedidos': pedidos})

@login_required
def lista_detallePedidos(request):
    detPedidos=DetallePedido.objects.all()
    return render(request, "lista_detallePedidos/index_detallePedido.html", {'detPedidos': detPedidos})

@login_required
def lista_detalleCompras(request):
    detCompras=DetalleCompra.objects.all()
    return render(request, "lista_detalleCompras/index_detalleCompra.html", {'detCompras': detCompras})

@login_required
def lista_mixCargas(request):
    mCargas=MixCarga.objects.all()
    return render(request, "lista_mixCargas/index_mixCarga.html", {'mCargas': mCargas})

@login_required
def lista_libroVentas(request):
    lVentas=LibroVentas.objects.all()
    return render(request, "lista_libroVentas/index_libroVenta.html", {'lVentas': lVentas})

@login_required
def lista_lDistribuidores(request):
    liDistribuidores=LiquidacionDistribucion.objects.all()
    return render(request, "lista_liquidacionDistribuidores/index_liquidacionDistribuidor.html", {'liDistribuidores': liDistribuidores})

@login_required
def lista_liquidacionVentas(request):
    liVentas=LiquidacionVentas.objects.all()
    return render(request, "lista_liquidacionVentas/index_liquidacionVenta.html", {'liVentas': liVentas})

@login_required
def lista_kardex(request):
    kardexs=Kardex.objects.all()
    return render(request, "lista_kardex/index_kardex.html", {'kardexs': kardexs})

@login_required
def lista_detalleFacturas(request):
    detFacturas=DetalleFactura.objects.all()
    return render(request, "lista_detalleFacturas/index_detalleFactura.html", {'detFacturas': detFacturas})

@login_required
def lista_facturas(request):
    facturas=Factura.objects.all()
    return render(request, "lista_facturas/index_factura.html", {'facturas': facturas})

@login_required
def lista_notaVentas(request):
    nVentas=NotaVenta.objects.all()
    return render(request, "lista_notaVentas/index_notaVenta.html", {'nVentas': nVentas})

@login_required
def lista_inventarios(request):
    inventarios=Inventario.objects.all()
    return render(request, "lista_inventarios/index_inventario.html", {'inventarios': inventarios})

@login_required
def personas(request):
    personas= Persona.objects.all()
    return render(request, "lista/index.html", {'personas': personas})

def tienda_view(request):
    personas= Persona.objects.all()
    return render(request, "lista/index.html", {'personas': personas})

def menu_view(request):
    return render(request, "paginas/menu.html")


def crear(request):
    formulario=PersonaForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista') 
    return render(request,'lista/crear.html',{'formulario':formulario})

def crear_producto(request):
    formulario=ProductoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_productos') 
    return render(request,'lista_productos/crear_producto.html',{'formulario':formulario})


def crear_ruta(request):
    formulario=RutaForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_rutas') 
    return render(request,'lista_rutas/crear_ruta.html',{'formulario':formulario})

def crear_distribuidor(request):
    formulario=DistribuidorForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_distribuidores') 
    return render(request,'lista_distribuidores/crear_distribuidor.html', {'formulario':formulario})

def crear_almacen(request):
    formulario=AlmacenForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_almacenes') 
    return render(request,'lista_almacenes/crear_almacen.html', {'formulario':formulario})

def crear_cCorporativa(request):
    formulario=CCorporativaForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_cCorporativas') 
    return render(request,'lista_cCorporativas/crear_cCorporativa.html', {'formulario':formulario})


def crear_pedido(request):
    formulario=PedidoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_pedidos') 
    return render(request,'lista_pedidos/crear_pedido.html', {'formulario':formulario})

def crear_detallePedido(request):
    formulario=DetallePedidoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_detallePedidos') 
    return render(request,'lista_detallePedidos/crear_detallePedido.html', {'formulario':formulario})


# views.py

def crear_detalleCompra(request):
    formulario = DetalleCompraForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        try:
            formulario.save()
            return redirect('lista_detalleCompras')
        except ValidationError as e:
            formulario.add_error(None, e.message)
    return render(request, 'lista_detalleCompras/crear_detalleCompra.html', {'formulario': formulario})


def crear_mixCarga(request):
    formulario=MixCargaForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_mixCargas') 
    return render(request,'lista_mixCargas/crear_mixCarga.html', {'formulario':formulario})

def crear_libroVenta(request):
    formulario=LibroVentasForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_libroVentas') 
    return render(request,'lista_libroVentas/crear_libroVenta.html', {'formulario':formulario})

def crear_liquidacionDistribuidor(request):
    formulario=LiquidacionDistribucionForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_liquidacionDistribuidores') 
    return render(request,'lista_liquidacionDistribuidores/crear_liquidacionDistribuidor.html', {'formulario':formulario})

def crear_liquidacionVenta(request):
    formulario=LiquidacionVentasForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_liquidacionVentas') 
    return render(request,'lista_liquidacionVentas/crear_liquidacionVenta.html', {'formulario':formulario})

def crear_inventario(request):
    formulario=InventarioForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_inventarios') 
    return render(request,'lista_inventarios/crear_inventario.html', {'formulario':formulario})

def crear_kardex(request):
    formulario=KardexForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_kardex') 
    return render(request,'lista_kardex/crear_kardex.html', {'formulario':formulario})

def crear_detalleFactura(request):
    formulario=DetalleFacturaForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_detalleFacturas') 
    return render(request,'lista_detalleFacturas/crear_detalleFactura.html', {'formulario':formulario})

def crear_factura(request):
    formulario=FacturaForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_facturas') 
    return render(request,'lista_facturas/crear_factura.html', {'formulario':formulario})

def crear_notaVenta(request):
    formulario=NotaVentaForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_notaVentas') 
    return render(request,'lista_notaVentas/crear_notaVenta.html', {'formulario':formulario})



def crear_crear_notaVenta(request):
    formulario=NotaVentaForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('lista_notaVentas') 
    return render(request,'lista_notaVentas/crear_notaVenta.html', {'formulario':formulario})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Usa el correo electrónico
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            
            if Persona.objects.get(email=email).rol == 'Cliente':
                login(request, user)
                return redirect('catalogoProductos')  # Redirige al menú principal
            elif Persona.objects.get(email=email).rol == 'Administrador':
                login(request, user)
                return redirect('menu')
        else:
            return render(request, 'paginas/login.html', {'error': 'Correo o contraseña incorrectos'})
    return render(request, 'paginas/login.html')

def contacto(request):
    if request.method == 'POST':
        form = MensajeContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'paginas/contacto.html', {
                'form': MensajeContactoForm(),  # limpia el formulario
                'mensaje_exito': 'Tu mensaje ha sido enviado con éxito.'
            })
    else:
        form = MensajeContactoForm()
    
    return render(request, 'paginas/contacto.html', {'form': form})

def enviar_contacto(request):
    if request.method == 'POST':
        form = MensajeContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu mensaje ha sido enviado con éxito.')
            return redirect('contacto')  # Vuelve a cargar la misma página
    else:
        form = MensajeContactoForm()

    return render(request, 'paginas/contacto.html', {'form': form})


def editar(request,id):
    persona=Persona.objects.get(id_persona=id)
    formulario=PersonaForm(request.POST or None, request.FILES or None, instance=persona)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('lista')
    return render(request,'lista/editar.html',{'formulario':formulario})


def editar_producto(request,id):
    producto=Producto.objects.get(id_producto=id)
    formulario=ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('lista_productos')
    return render(request,'lista_productos/editar_producto.html',{'formulario':formulario})

def editar_ruta(request,id):
    ruta=Ruta.objects.get(id_ruta=id)
    formulario=RutaForm(request.POST or None, request.FILES or None, instance=ruta)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('lista_rutas')
    return render(request,'lista_rutas/editar_ruta.html',{'formulario':formulario})

def editar_distribuidor(request,id):
    distribuidor=Distribuidor.objects.get(id_distribuidor=id)
    formulario=DistribuidorForm(request.POST or None, request.FILES or None, instance=distribuidor)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('lista_distribuidores')
    return render(request,'lista_distribuidores/editar_distribuidor.html',{'formulario':formulario})

def editar_almacen(request,id):
    almacen=Almacen.objects.get(id_almacen=id)
    formulario=AlmacenForm(request.POST or None, request.FILES or None, instance=almacen)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('lista_almacenes')
    return render(request,'lista_almacenes/editar_almacen.html',{'formulario':formulario})

def editar_cCorporativa(request, id):
    compra = get_object_or_404(CompraCorporativa, id_compra_corporativa=id)
    formulario = CCorporativaForm(request.POST or None, instance=compra)
    
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('lista_cCorporativas')
    
    return render(request, 'lista_cCorporativas/editar_cCorporativa.html', {
        'formulario': formulario,
        'compra': compra
    })
    
    
def editar_pedido(request,id):
    pedido=Pedido.objects.get(id_pedido=id)
    formulario=PedidoForm(request.POST or None, request.FILES or None, instance=pedido)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('lista_pedidos')
    return render(request,'lista_pedidos/editar_pedido.html',{'formulario':formulario})

def editar_detallePedido(request,id):
    detPedido=DetallePedido.objects.get(id_detalle_pedido=id)
    formulario=DetallePedidoForm(request.POST or None, request.FILES or None, instance=detPedido)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('lista_detallePedidos')
    return render(request,'lista_detallePedidos/editar_detallePedido.html',{'formulario':formulario})

def editar_detalleCompra(request,id):
    detCompra=DetalleCompra.objects.get(id_detalle_compra=id)
    formulario=DetalleCompraForm(request.POST or None, request.FILES or None, instance=detCompra)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('lista_detalleCompras')
    return render(request,'lista_detalleCompras/editar_detalleCompra.html',{'formulario':formulario})

def editar_mixCarga(request,id):
    mCarga=MixCarga.objects.get(id_mix_carga=id)
    formulario=MixCargaForm(request.POST or None, request.FILES or None, instance=mCarga)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('lista_mixCargas')
    return render(request,'lista_mixCargas/editar_mixCarga.html',{'formulario':formulario})


def editar_libroVenta(request,id):
    lVenta=LibroVentas.objects.get(id_libro_ventas=id)
    formulario=LibroVentasForm(request.POST or None, request.FILES or None, instance=lVenta)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('lista_libroVentas')
    return render(request,'lista_libroVentas/editar_libroVenta.html',{'formulario':formulario})

def editar_lDistribuidor(request,id):
    liDistribuidor=LiquidacionDistribucion.objects.get(id_liquidacion_distribucion=id)
    formulario=LiquidacionDistribucionForm(request.POST or None, request.FILES or None, instance=liDistribuidor)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('lista_liquidacionDistribuidores')
    return render(request,'lista_liquidacionDistribuidores/editar_lDistribuidor.html',{'formulario':formulario})

def editar_liquidacionVenta(request,id):
    liVenta=LiquidacionVentas.objects.get(id_liquidacion_ventas=id)
    formulario=LiquidacionVentasForm(request.POST or None, request.FILES or None, instance=liVenta)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('lista_liquidacionVentas')
    return render(request,'lista_liquidacionVentas/editar_liquidacionVenta.html',{'formulario':formulario})

def editar_inventario(request,id):
    inventario=Inventario.objects.get(id_inventario=id)
    formulario=InventarioForm(request.POST or None, request.FILES or None, instance=inventario)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('lista_inventarios')
    return render(request,'lista_inventarios/editar_inventario.html',{'formulario':formulario})

def editar_kardex(request,id):
    kardex=Kardex.objects.get(id_kardex=id)
    formulario=KardexForm(request.POST or None, request.FILES or None, instance=kardex)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('lista_kardex')
    return render(request,'lista_kardex/editar_kardex.html',{'formulario':formulario})


def editar_detalleFactura(request,id):
    detFactura=DetalleFactura.objects.get(id_detalle_factura=id)
    formulario=DetalleFacturaForm(request.POST or None, request.FILES or None, instance=detFactura)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('lista_detalleFacturas')
    return render(request,'lista_detalleFacturas/editar_detalleFactura.html',{'formulario':formulario})

def editar_factura(request,id):
    factura=Factura.objects.get(id_factura=id)
    formulario=FacturaForm(request.POST or None, request.FILES or None, instance=factura)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('lista_facturas')
    return render(request,'lista_facturas/editar_factura.html',{'formulario':formulario})

def editar_notaVenta(request,id):
    nVenta=NotaVenta.objects.get(id_nota_venta=id)
    formulario=NotaVentaForm(request.POST or None, request.FILES or None, instance=nVenta)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('lista_notaVentas')
    return render(request,'lista_notaVentas/editar_notaVenta.html',{'formulario':formulario})


def eliminar(request, id):
    persona=Persona.objects.get(id_persona=id)
    persona.delete()
    return redirect('lista')

def eliminar_producto(request, id):
    producto=Producto.objects.get(id_producto=id)
    producto.delete()
    return redirect('lista_productos')

def eliminar_almacen(request, id):
    almacen=Almacen.objects.get(id_almacen=id)
    almacen.delete()
    return redirect('lista_almacenes')


def eliminar_cCorporativa(request, id):
    compra = get_object_or_404(CompraCorporativa, id_compra_corporativa=id)
    
    if request.method == 'POST':
        # Revertir stock de todos los detalles
        for detalle in compra.detallecompra_set.all():
            producto = detalle.id_producto
            producto.stock -= detalle.cantidad
            producto.save()
            
            # Registrar en Kardex (Salida)
            Kardex.objects.create(
                producto=producto,
                tipo_movimiento='Salida',
                cantidad=detalle.cantidad,
                stockFinal=producto.stock,
                idAlmacen=producto.id_almacen
            )
        
        compra.delete()
        return redirect('lista_cCorporativas')
    
    return render(request, 'confirmar_eliminacion_cCorporativa.html', {'compra': compra})


def eliminar_pedido(request, id):
    pedido=Pedido.objects.get(id_pedido=id)
    pedido.delete()
    return redirect('lista_pedidos')

def eliminar_detallePedido(request, id):
    detPedido=DetallePedido.objects.get(id_detalle_pedido=id)
    detPedido.delete()
    return redirect('lista_detallePedidos')

def eliminar_detalleCompra(request, id):
    detalle = get_object_or_404(DetalleCompra, id_detalle_compra=id)
    compra = detalle.id_compraCorporativa
       
    # Revertir stock del producto
    producto = detalle.id_producto
    producto.stock -= detalle.cantidad
    producto.save()
        
    # Registrar en Kardex (Salida)
    Kardex.objects.create(
        producto=producto,
        tipo_movimiento='Salida',
        cantidad=detalle.cantidad,
        stockFinal=producto.stock,
        idAlmacen=producto.id_almacen
    )
    
    # Eliminar el detalle
    detalle.delete()

    # Redirigir a la lista de detalles de compra
    return redirect('lista_detalleCompras')


def eliminar_mixCarga(request, id):
    mCarga=MixCarga.objects.get(id_mix_carga=id)
    mCarga.delete()
    return redirect('lista_mixCargas')

def eliminar_libroVenta(request, id):
    lVenta=LibroVentas.objects.get(id_libro_ventas=id)
    lVenta.delete()
    return redirect('lista_libroVentas')

def eliminar_liquidacionDistribuidor(request, id):
    liDistribuidor=LiquidacionDistribucion.objects.get(id_liquidacion_distribucion=id)
    liDistribuidor.delete()
    return redirect('lista_liquidacionDistribuidores')

def eliminar_liquidacionVenta(request, id):
    liVenta=LiquidacionVentas.objects.get(id_liquidacion_ventas=id)
    liVenta.delete()
    return redirect('lista_liquidacionVentas')

def eliminar_inventario(request, id):
    inventario=LiquidacionVentas.objects.get(id_inventario=id)
    inventario.delete()
    return redirect('lista_inventarios')

def eliminar_kardex(request, id):
    kardex=Kardex.objects.get(id_kardex=id)
    kardex.delete()
    return redirect('lista_kardex')

def eliminar_detalleFactura(request, id):
    detFactura=DetalleFactura.objects.get(id_detalle_factura=id)
    detFactura.delete()
    return redirect('lista_detalleFacturas')

def eliminar_factura(request, id):
    factura=Factura.objects.get(id_factura=id)
    factura.delete()
    return redirect('lista_facturas')

def eliminar_notaVenta(request, id):
    notaVenta=NotaVenta.objects.get(id_nota_venta=id)
    notaVenta.delete()
    return redirect('lista_notaVentas')

def eliminar_distribuidor(request, id):
    distribuidor=Distribuidor.objects.get(id_distribuidor=id)
    distribuidor.delete()
    return redirect('lista_distribuidores')

def eliminar_producto(request, id):
    producto=Producto.objects.get(id_producto=id)
    producto.delete()
    return redirect('lista_productos')

def eliminar_ruta(request, id):
    ruta=Ruta.objects.get(id_ruta=id)
    ruta.delete()
    return redirect('lista_rutas')

def imagen_papa(request):
    return HttpResponse(open(settings.BASE_DIR / 'imagenes/papa.png', 'rb').read(), content_type='image/png')

# views.py
def actualizar_cantidad(request, item_id):
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        carrito = request.session.get('carrito', {})
        if str(item_id) in carrito and cantidad > 0:
            carrito[str(item_id)]['cantidad'] = cantidad
            request.session['carrito'] = carrito
    return redirect('carrito')


def eliminar_del_carrito(request, item_id):
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        if str(item_id) in carrito:
            del carrito[str(item_id)]
            request.session['carrito'] = carrito
    return redirect('carrito')
      
      
      
      

def format_number(value):
    """Formatea números con separador de miles"""
    if value is None:
        return ''
    return '{:,}'.format(int(value)).replace(',', '.')


@login_required
def descargar_factura(request, factura_id):
    try:
        # Obtener la factura
        factura = Factura.objects.get(id_factura=factura_id)
        
        # Obtener detalles del pedido asociado a la factura
        detalles_pedido = DetallePedido.objects.filter(idPedido=factura.idPedido)
        
        # Datos de empresa (ajustar según tu información real)
        datos_empresa = {
            'nombre': 'Industrias San Miguel de Arica S.A.C.',
            'direccion': 'Av. Argentina 2997, Arica',
            'telefono': ' (+56) 800-914-223',
            'email': 'atencionalcliente@ism.global',
            'web': 'www.ism.arica.com',
            'rut': '76.123.456-5',
            'giro': 'Venta de productos bebestibles'
        }

        # Validación de número negativo
        if factura.totalBruto < 0:
            total_letras = "NEGATIVO " + numero_a_palabras(abs(int(factura.totalBruto)))
        else:
            total_letras = numero_a_palabras(int(factura.totalBruto))
        
        # Crear respuesta HTTP con tipo PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="factura_{factura.numeroFactura}.pdf"'
        
        # Crear documento PDF
        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter
        styles = getSampleStyleSheet()
        
        # Encabezado
        p.setFont("Helvetica-Bold", 16)
        p.setFillColorRGB(0, 0.4, 0.7)  # Azul profesional
        p.drawString(50, height - 50, datos_empresa['nombre'])
        p.setFont("Helvetica", 10)
        p.setFillColorRGB(0, 0, 0)  # Negro
        p.drawString(50, height - 65, f"Giro: {datos_empresa['giro']}")
        p.drawString(50, height - 80, f"RUT: {datos_empresa['rut']}")
        p.drawString(50, height - 95, f"Dirección: {datos_empresa['direccion']}")
        p.drawString(50, height - 110, f"Teléfono: {datos_empresa['telefono']} | Email: {datos_empresa['email']}")
        
        # Datos cliente
        p.setFont("Helvetica-Bold", 12)
        p.drawString(300, height - 65, "FACTURA ELECTRÓNICA")
        p.setFont("Helvetica", 10)
        p.drawString(300, height - 80, f"Nº {factura.numeroFactura}")
        p.drawString(300, height - 95, f"Fecha emisión: {factura.fechaEmision.strftime('%d/%m/%Y')}")

        # Datos cliente
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, height - 140, "Señor(es):")
        p.setFont("Helvetica", 10)
        p.drawString(50, height - 155, factura.razon_social)
        p.drawString(50, height - 170, f"RUT: {factura.rut}")
        p.drawString(50, height - 185, f"Dirección: {factura.direccion_fiscal}")

        # Documento Tributario
        p.setFont("Helvetica-Bold", 10)
        p.drawString(300, height - 140, "Documento Tributario:")
        p.setFont("Helvetica", 10)
        p.drawString(300, height - 155, f"Tipo: {factura.tipoDocumento}")
        p.drawString(300, height - 170, f"RUT Emisor: {datos_empresa['rut']}")
        p.drawString(300, height - 185, "Código Sucursal: 0")

        # Tabla de items
        data = [["Cantidad", "Unidad", "Descripción", "Precio Unitario", "Total"]]
        
        for detalle_pedido in detalles_pedido:
            data.append([
                str(detalle_pedido.cantidad),
                "UN",
                detalle_pedido.idProducto.descripcion[:30] + "..." if len(detalle_pedido.idProducto.descripcion) > 30 else detalle_pedido.idProducto.descripcion,
                f"${int(detalle_pedido.precioUnitario)}",
                f"${int(detalle_pedido.subtotal)}"
            ])

        table = Table(data, colWidths=[60, 50, 200, 80, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0, 0.4, 0.7)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        table.wrapOn(p, width, height)
        table.drawOn(p, 50, height - 220)

        # Totales
        y = height - 240
        p.setFont("Helvetica-Bold", 10)
        p.drawString(400, y, "Subtotal:")
        #p.drawString(400, y - 15, "IVA 19%:")
        p.drawString(400, y - 30, "TOTAL:")
        
        p.setFont("Helvetica", 10)
        p.drawString(480, y, f"${int(factura.totalBruto)}")
        #p.drawString(480, y - 15, f"${int(factura.iva)}")
        p.setFont("Helvetica-Bold", 12)
        p.setFillColorRGB(0, 0.5, 0)  # Verde profesional
        p.drawString(480, y - 30, f"${int(factura.totalBruto)}")
        
        # Total en letras
        p.setFillColorRGB(0, 0.4, 0.7)
        p.setFont("Helvetica-Bold", 8)
        p.drawString(50, y - 50, f"SON {total_letras.upper()} PESOS")
        
        # Información adicional
        p.setFillColorRGB(0, 0, 0)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y - 80, "Condiciones de pago:")
        p.setFont("Helvetica", 10)
        p.drawString(50, y - 95, "Pago en efectivo o transferencia bancaria")

        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y - 110, "Forma de pago:")
        p.setFont("Helvetica", 10)
        p.drawString(50, y - 125, "Contado")

        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y - 140, "Observaciones:")
        p.setFont("Helvetica", 10)
        p.drawString(50, y - 155, "No se aceptan devoluciones después de 7 días")

        # Pie de página con información SII
        p.setFont("Helvetica", 8)
        p.drawString(50, 50, "Este documento es un documento tributario electrónico emitido por el sistema de facturación electrónica de Distribuidora Industrias San Miguel de Arica.")
        p.drawString(50, 40, "Documento válido para crédito fiscal y para respaldo de gasto efectivo")
        p.drawString(50, 30, "Para validar este documento visite www.sii.cl")

        p.showPage()
        p.save()
        return response
        
    except Factura.DoesNotExist:
        return HttpResponse("Factura no encontrada", status=404)

# Configuración de logging
logger = logging.getLogger(__name__)

# --- Helper para configuración compartida ---
def get_transbank_transaction():
    """
    Retorna una instancia configurada de Transaction
    """
    return Transaction(
        WebpayOptions(
            commerce_code=settings.TRANSBANK_COMMERCE_CODE,
            api_key=settings.TRANSBANK_API_KEY,
            environment=getattr(settings, 'TRANSBANK_ENVIRONMENT', 'INTEGRATION')
        )
    )
    
def iniciar_pago(request):
    # Configuración de Transbank (usa tus credenciales reales o las de prueba)
    commerce_code = settings.TRANSBANK_COMMERCE_CODE
    api_key = settings.TRANSBANK_API_KEY
    environment = "INTEGRATION"  # "LIVE" para producción
    
    # Configuración obligatoria que faltaba
    tx = Transaction(
        WebpayOptions(commerce_code, api_key, environment)
    )
    
    carrito = request.session.get('carrito', {})
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    
    try:
        response = tx.create(
            buy_order=f"BO_{request.session.session_key[:10]}",  # Ej: "BO_sess12345"
            session_id=request.session.session_key,
            amount=total,
            return_url=settings.TRANSBANK_RETURN_URL
        )
        return redirect(response['url'] + "?token_ws=" + response['token'])
    
    except Exception as e:
        # Manejo de errores adecuado
        print(f"Error Transbank: {str(e)}")
        return render(request, 'error_pago.html', {'error': str(e)})
    
# views.py

def retorno_pago(request):
    
    
    # Configuración de Transbank (la misma que en iniciar_pago)
    commerce_code = settings.TRANSBANK_COMMERCE_CODE
    api_key = settings.TRANSBANK_API_KEY
    environment = "INTEGRATION"  # "LIVE" en producción
    
    tx = Transaction(
        WebpayOptions(commerce_code, api_key, environment)
    )
    
    token = request.GET.get('token_ws')
    
    
    
    
    if not token:
        return render(request, 'tienda/pago_error.html', {
            'error': 'Token no recibido desde Transbank'
        })
    
    try:
        response = tx.commit(token=token)
        if response.get('status') == 'AUTHORIZED':
            carrito = request.session.get('carrito', {})
            
            # 1. Obtener datos básicos (fuera del bucle)
            ruta_predeterminada = Ruta.objects.first()
            cliente = Persona.objects.get(id_persona=request.user.id_persona)
            total_pedido = 0
            detalles_pedido = []
            
            # 2. Crear Pedido (antes del bucle)
            pedido = Pedido.objects.create(
                id_cliente=cliente,
                fecha_pedido=timezone.now(),
                estado='Completado',
                id_ruta=ruta_predeterminada,
                total=0  # Se actualizará después
            )
            
            # 3. Procesar items del carrito
            for item_id, item_data in carrito.items():
                producto = Producto.objects.get(id_producto=item_id)
                cantidad = item_data['cantidad']
                subtotal = cantidad * float(producto.precio)
                
                DetallePedido.objects.create(
                    idPedido=pedido,
                    idProducto=producto,
                    cantidad=cantidad,
                    precioUnitario=producto.precio,
                    subtotal=subtotal
                )
                
                total_pedido += subtotal
                
                # Actualizar stock
                producto.stock -= cantidad
                producto.save()
                
                # Registrar en Kardex
                Kardex.objects.create(
                    producto=producto,
                    tipo_movimiento='Salida',
                    cantidad=cantidad,
                    stockFinal=producto.stock,
                    idAlmacen=Almacen.objects.first()
                )
            
            # 4. Actualizar total del pedido (fuera del bucle)
            pedido.total = total_pedido
            pedido.save()
            
            # 5. Crear documentos (SOLO UNA VEZ)
            factura = Factura.objects.create(
                numeroFactura=f"FACT-{pedido.id_pedido}",
                totalBruto=total_pedido,
                idPedido=pedido,
                estado='Completado',
                razon_social=f"{cliente.nombres} {cliente.apellidos}",
                rut=cliente.rut
            )
            
            # 6. Crear detalles de factura
            for detalle in DetallePedido.objects.filter(idPedido=pedido):
                DetalleFactura.objects.create(
                    idProducto=detalle.idProducto,
                    cantidad=detalle.cantidad,
                    precioUnitario=detalle.precioUnitario,
                    subtotal=detalle.subtotal,
                    id_factura=factura
                )
            
            # 7. Nota de venta
            NotaVenta.objects.create(
                totalBruto=total_pedido,
                id_factura=factura,
                estado='Completado'
            )
            
            # 8. Limpiar carrito
            request.session['carrito'] = {}
            
            # Debug importante
            logger.info(f"Pedido {pedido.id_pedido} creado exitosamente")
            
            return render(request, 'tienda/pago_exitoso.html', {
                'pedido': pedido,
                'factura': factura,
                'response': response
            })
        else:
            # Pago rechazado
            return render(request, 'tienda/pago_rechazado.html', {
                'response': response
            })
            
    except Exception as e:
        # Error en la transacción
        return render(request, 'tienda/pago_error.html', {
            'error': str(e),
            'token': token
        })
        
def pago_exitoso(request, factura_id):
    factura = get_object_or_404(Factura, id_factura=factura_id)
    return render(request, 'tienda/pago_exitoso.html', {
        'factura': factura
    })
    

def listar_mensajes(request):
    mensajes = MensajeContacto.objects.all().order_by('-fecha_envio')  # Más recientes primero
    return render(request, 'paginas/mensajesClientes.html', {'mensajes': mensajes})

@login_required
def perfil_usuario(request):
    usuario = request.user

    if request.method == 'POST':
        if 'actualizar_datos' in request.POST:
            form = PerfilForm(request.POST, instance=usuario)
            pass_form = PasswordChangeForm(usuario)
            if form.is_valid():
                form.save()
                messages.success(request, 'Datos actualizados correctamente.')
                return redirect('perfil_usuario')

        elif 'actualizar_password' in request.POST:
            form = PerfilForm(instance=usuario)
            pass_form = PasswordChangeForm(usuario, request.POST)
            if pass_form.is_valid():
                user = pass_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Contraseña actualizada correctamente.')
                return redirect('perfil_usuario')
            else:
                print(pass_form.errors)  # Para depurar en consola    
                messages.error(request, 'Error al actualizar la contraseña. Verifica los datos.')

        else:
            form = PerfilForm(instance=usuario)
            pass_form = PasswordChangeForm(usuario)
    else:
        form = PerfilForm(instance=usuario)
        pass_form = PasswordChangeForm(usuario)

    return render(request, 'paginas/perfil.html', {
        'form': form,
        'pass_form': pass_form
    })