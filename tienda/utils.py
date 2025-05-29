def calcular_dv(rut):
    rut = list(map(int, str(rut)))[::-1]  # Invierte el RUT
    secuencia = [2, 3, 4, 5, 6, 7]  # Secuencia repetitiva
    total = 0

    for i, digito in enumerate(rut):
        total += digito * secuencia[i % len(secuencia)]

    resto = total % 11
    dv = 11 - resto

    if dv == 11:
        return '0'
    elif dv == 10:
        return 'K'
    else:
        return str(dv)


def calcular_subtotal(cantidad, precio_unitario, descuento=0, impuesto=None):
    """
    Calcula el subtotal para un detalle.
    
    Args:
        cantidad (int): Cantidad de productos
        precio_unitario (Decimal): Precio unitario del producto
        descuento (Decimal, opcional): Descuento aplicado al detalle. Por defecto es 0.
        impuesto (str, opcional): Código de impuesto aplicado. Por defecto es None.
    
    Returns:
        Decimal: El subtotal calculado
    """
    from decimal import Decimal
    
    # Cálculo base: cantidad * precio_unitario - descuento
    subtotal_base = Decimal((cantidad * precio_unitario) - descuento)
    
    # Si no hay impuesto especificado o está vacío, retornamos el cálculo base
    if not impuesto:
        return subtotal_base
    
    # Aquí puedes implementar la lógica de impuestos según tus necesidades
    # Por ejemplo, podríamos tener un diccionario con los porcentajes de impuestos
    impuestos = {
        'IVA16': Decimal('0.16'),
        'IVA8': Decimal('0.08'),
        'IEPS': Decimal('0.30'),
        # Añade más impuestos según sea necesario
    }
    
    # Si el impuesto está en nuestro diccionario, lo aplicamos
    tasa_impuesto = impuestos.get(impuesto, Decimal('0'))
    monto_impuesto = Decimal(subtotal_base) * tasa_impuesto
    
    return subtotal_base + monto_impuesto


def actualizar_subtotales_pedido(pedido):
    """
    Actualiza los subtotales de todos los detalles de un pedido específico
    y devuelve el total del pedido.
    
    Args:
        pedido (Pedido): Objeto del modelo Pedido
    
    Returns:
        Decimal: El total del pedido (suma de todos los subtotales)
    """
    from decimal import Decimal
    detalles = pedido.detallepedido_set.all()
    total = Decimal('0.00')
    
    for detalle in detalles:
        detalle.subtotal = calcular_subtotal(
            detalle.cantidad, 
            detalle.precioUnitario, 
            detalle.descuento
        )
        detalle.save()
        total += detalle.subtotal
    
    return total


def actualizar_todos_subtotales():
    """
    Actualiza los subtotales de todos los detalles de pedidos en la base de datos.
    
    Returns:
        int: Número de detalles actualizados
    """
    from .models import DetallePedido
    
    detalles = DetallePedido.objects.all()
    contador = 0
    
    for detalle in detalles:
        detalle.subtotal = calcular_subtotal(
            detalle.cantidad, 
            detalle.precioUnitario, 
            detalle.descuento
        )
        detalle.save()
        contador += 1
    
    return contador


# Nuevas funciones para DetalleCompra
def actualizar_subtotales_compra(compra):
    """
    Actualiza los subtotales de todos los detalles de una compra corporativa específica
    y devuelve el total de la compra.
    
    Args:
        compra (CompraCorporativa): Objeto del modelo CompraCorporativa
    
    Returns:
        Decimal: El total de la compra (suma de todos los subtotales)
    """
    from decimal import Decimal
    detalles = compra.detallecompra_set.all()
    total = Decimal('0.00')
    
    for detalle in detalles:
        detalle.subtotal = calcular_subtotal(
            detalle.cantidad, 
            detalle.precioUnitario, 
            detalle.descuento
        )
        detalle.save()
        total += detalle.subtotal
    
    return total


def actualizar_todos_subtotales_compras():
    """
    Actualiza los subtotales de todos los detalles de compras en la base de datos.
    
    Returns:
        int: Número de detalles actualizados
    """
    from .models import DetalleCompra
    
    detalles = DetalleCompra.objects.all()
    contador = 0
    
    for detalle in detalles:
        detalle.subtotal = calcular_subtotal(
            detalle.cantidad, 
            detalle.precioUnitario, 
            detalle.descuento
        )
        detalle.save()
        contador += 1
    
    return contador



# Nuevas funciones para DetalleFactura
def actualizar_subtotales_factura(factura):
    """
    Actualiza los subtotales de todos los detalles de una factura específica
    y devuelve el total de la factura.
    
    Args:
        factura (Factura): Objeto del modelo Factura
    
    Returns:
        Decimal: El total de la factura (suma de todos los subtotales)
    """
    from decimal import Decimal
    detalles = factura.detallefactura_set.all()
    total = Decimal('0.00')
    
    for detalle in detalles:
        detalle.subtotal = calcular_subtotal(
            detalle.cantidad, 
            detalle.precioUnitario, 
            detalle.descuento,
            detalle.impuestoAplicado
        )
        detalle.save()
        total += detalle.subtotal
    
    return total


def actualizar_todos_subtotales_facturas():
    """
    Actualiza los subtotales de todos los detalles de facturas en la base de datos.
    
    Returns:
        int: Número de detalles actualizados
    """
    from .models import DetalleFactura
    
    detalles = DetalleFactura.objects.all()
    contador = 0
    
    for detalle in detalles:
        detalle.subtotal = calcular_subtotal(
            detalle.cantidad, 
            detalle.precioUnitario, 
            detalle.descuento,
            detalle.impuestoAplicado
        )
        detalle.save()
        contador += 1
    
    return contador


# utils.py
def format_number(value):
    return '{:,}'.format(int(value)).replace(',', '.')


def numero_a_palabras(numero):
    """Convierte un número a palabras (en español)"""
    unidades = ['', 'UN ', 'DOS ', 'TRES ', 'CUATRO ', 'CINCO ', 'SEIS ', 'SIETE ', 'OCHO ', 'NUEVE ']
    decenas = ['', 'DIEZ ', 'VEINTE ', 'TREINTA ', 'CUARENTA ', 'CINCUENTA ', 'SESENTA ', 'SETENTA ', 'OCHENTA ', 'NOVENTA ']
    centenas = ['', 'CIENTO ', 'DOSCIENTOS ', 'TRESCIENTOS ', 'CUATROCIENTOS ', 'QUINIENTOS ', 'SEISCIENTOS ', 'SETECIENTOS ', 'OCHOCIENTOS ', 'NOVECIENTOS ']

    if numero == 0:
        return "CERO"

    en_palabras = ''
    temp_numero = numero

    if temp_numero < 0:
        en_palabras += "MENOS "
        temp_numero = abs(temp_numero)

    if (temp_numero // 1000000) > 0:
        en_palabras += numero_a_palabras(temp_numero // 1000000) + "MILLONES "
        temp_numero = temp_numero % 1000000

    if (temp_numero // 1000) > 0:
        en_palabras += numero_a_palabras(temp_numero // 1000) + "MIL "
        temp_numero = temp_numero % 1000

    if (temp_numero // 100) > 0:
        en_palabras += centenas[temp_numero // 100]
        temp_numero = temp_numero % 100

    if (temp_numero // 10) > 0:
        decena = temp_numero // 10
        if temp_numero % 10 == 0:
            en_palabras += decenas[decena]
        else:
            en_palabras += decenas[decena] + 'Y '
        temp_numero = temp_numero % 10

    if temp_numero > 0:
        en_palabras += unidades[temp_numero]

    return en_palabras.strip()