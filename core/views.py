from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Sum, F
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from collections import defaultdict
from datetime import date
from .models import Prestamos, Clientes, Pagos, TipodePago, Moneda, TasaCambio
from .forms import ClienteForm, PasswordVerificationForm, PrestamosForm, PagosForm, TasaForm
import json

@login_required
def home(request):
    context = {'mensaje':'error', 
            'prestamos': prestamos,
            'user_is_authenticated': request.user.is_authenticated}
    return redirect('prestamos')

# ---------- Clientes ----------
@login_required
def clientes(request):
    if request.method == 'GET':
        clientes = Clientes.objects.all()
        form = ClienteForm()

        # Agregar atributos dinámicos a cada cliente
        for cliente in clientes:
            cliente.prestamos_activos = Prestamos.contar_prestamos_activos(cliente)
            cliente.prestamos_pagados = Prestamos.contar_prestamos_pagados(cliente)
        
        
        context = {'clientes': clientes,
                'pagos': pagos,
                'form': form,
                'user_is_authenticated': request.user.is_authenticated}
        return render(request, 'clientes/clientes.html', context)

@login_required
def cliente_crear(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)  # No guardar aún para asignar el usuario
            cliente.ultimo_usuario_modificacion = request.user  # Asignar el usuario actual
            cliente.save()  # Guardar el cliente con el usuario asignado
            return redirect('clientes')  # Redirige a la lista de clientes
        else:
            # Si el formulario no es válido, se pasa el formulario con errores al contexto
            context = {
                'form': form,
                'errors': form.errors,  # Incluye los errores del formulario
                 'user_is_authenticated': request.user.is_authenticated,
            }
            return render(request, 'clientes/cliente_crear.html', context)
    else:
        form = ClienteForm()
    
    context = {
        'form': form,
         'user_is_authenticated': request.user.is_authenticated
    }
    return render(request, 'clientes/cliente_crear.html', context)

@login_required
def cliente_borrar(request, cliente_id):
    cliente = Clientes.objects.get(id=cliente_id)
    if request.method == "POST":
        form = PasswordVerificationForm(request.user, request.POST)
        if form.is_valid():
            cliente.delete()
            return redirect('clientes')
        else:
            form = PasswordVerificationForm(request.user)
            
    form = PasswordVerificationForm(request.user)
    context = {
            'form': form, 
            'cliente': cliente,
            'error': 'Contraseña incorrecta',
            'user_is_authenticated': request.user.is_authenticated}
    return render(request, 'clientes/cliente_borrar.html', context)

def prestamo_detalles_api(request, id):
    prestamo = get_object_or_404(Prestamos, id=id)
    data = {
        'monto_prestamo': prestamo.monto_prestamo,
        'monto_pago': prestamo.monto_pago,
        'monto_a_pagar': prestamo.monto_pago - prestamo.monto_a_pagar,
    }
    return JsonResponse(data)

@login_required
def cliente_detalles(request, cliente_id):
    cliente = get_object_or_404(Clientes, id=cliente_id)
    clientes = Clientes.objects.all()
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('cliente_detalles', cliente_id=cliente.id)
        else:
            print(form.errors)
    else:
        form = ClienteForm(instance=cliente)
    
    prestamos = cliente.prestamos_set.all()
    pagos = Pagos.objects.filter(cliente=cliente)
    ultimo_pago = pagos.first()
    fecha_ultimo_pago = ultimo_pago.fecha_pago if ultimo_pago else None
    prestamos_activos = Prestamos.contar_prestamos_activos(cliente)
    prestamos_pagados = Prestamos.contar_prestamos_pagados(cliente)
    balance = Prestamos.calcular_balance_total(cliente)
    balance_total = Prestamos.suma_total_prestamos(cliente)
    tasa_interes_total = Prestamos.tasa_interes_total(cliente)
    total_monto_a_pagar = sum(prestamo.monto_a_pagar for prestamo in prestamos)
    
    context = {
        'cliente': cliente,
        'clientes': clientes,
        'prestamos': prestamos,
        'pagos': pagos,
        'balance': balance,
        'balance_total': balance_total,
        'fecha_ultimo_pago': fecha_ultimo_pago,
        'prestamos_activos': prestamos_activos,
        'prestamos_pagados': prestamos_pagados,
        'total_monto_a_pagar': total_monto_a_pagar,
        'tasa_interes_total': tasa_interes_total,
        'form': form,
        'user_is_authenticated': request.user.is_authenticated
    }
    
    return render(request, 'clientes/cliente_detalles.html', context)
        
@login_required
def cliente_editar(request, cliente_id):
    cliente = get_object_or_404(Clientes, id=cliente_id)
    
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            #guarda el ultimo usuario que modifico al cliente al guardar cambios
            cliente.ultimo_usuario_modificacion = request.user 
            cliente.save
            return redirect('cliente_detalles', cliente_id=cliente.id)  # Redirigir a la página de detalles del cliente
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'clientes/cliente_editar.html', {'form': form, 'cliente': cliente, 'user_is_authenticated': request.user.is_authenticated})

# prestamos 
def obtener_prestamos_pagados_por_dia():
    # Obtener préstamos pagados agrupados por fecha
    prestamos_pagados = Prestamos.objects.filter(fecha_pago__isnull=False)
    prestamos_por_dia = prestamos_pagados.values('fecha_pago').annotate(total=Count('id')).order_by('fecha_pago')
    
    # Preparar datos para el gráfico
    fechas = [prestamo['fecha_pago'].strftime('%Y-%m-%d') for prestamo in prestamos_por_dia]
    totales = [prestamo['total'] for prestamo in prestamos_por_dia]

    return {
        'fechas': fechas,
        'totales': totales,
    }
    
def obtener_montos_pagados_por_dia():
    # Obtener montos pagados agrupados por fecha
    montos_pagados = Prestamos.objects.filter(fecha_pago__isnull=False)
    montos_por_dia = montos_pagados.values('fecha_pago').annotate(total=Sum('monto_pago')).distinct().order_by('fecha_pago')

    #ordenar fechas
    montos_por_dia = sorted(montos_por_dia, key=lambda x: x['fecha_pago'])
    # Preparar datos para el gráfico
    fechas = [monto['fecha_pago'].strftime('%Y-%m-%d') for monto in montos_por_dia]
    totales = [float(monto['total']) for monto in montos_por_dia]

    return {
        'fechas': fechas,
        'totales': totales,
    }
    
# ---------- Prestamos ----------
@login_required
def prestamos(request):
    if request.method == 'GET':
        prestamos_pagados = Prestamos.objects.filter(pagado=True)
        prestamos_sin_pagar = Prestamos.objects.filter(pagado=False)
        
        #función para obtener los préstamos pagados por día
        data_prestamos_pagados = obtener_prestamos_pagados_por_dia()
        data_montos_pagados = obtener_montos_pagados_por_dia()
        
        # Agrupar por fecha y calcular totales
        data = defaultdict(float)
        for prestamo in prestamos_pagados:
            fecha = prestamo.fecha_pago.strftime('%Y-%m-%d')  # Formato de fecha
            data[fecha] += float(prestamo.monto_pago)

        # Convertir a listas para JSON
        fechas = list(data.keys())
        totales = list(data.values())
        
        # Convertir los datos a JSON
        data_json_dia = json.dumps(data_prestamos_pagados)
        data_json_montos = json.dumps(data_montos_pagados)
        data_json = json.dumps({'fechas': fechas, 'totales': totales})
        
        context = {'mensaje':'mensaje', 
                    'prestamos_sin_pagar': prestamos_sin_pagar,
                    'prestamos_pagados': prestamos_pagados,
                    'data_json': data_json,
                    'data_json_dia': data_json_dia,
                    'data_json_montos' : data_json_montos,
                    'user_is_authenticated': request.user.is_authenticated}
        return render(request, 'prestamos/prestamos.html', context)
    
@login_required
def prestamo_detalles(request, prestamo_id):
    prestamo = get_object_or_404(Prestamos, pk=prestamo_id)
    cedula_cliente = prestamo.cliente.cedula
    context = {
        'prestamo': prestamo,
        'cedula_cliente': cedula_cliente,
        'user_is_authenticated': request.user.is_authenticated,
    }
    return render(request, 'prestamos/prestamo_detalles.html', context)

def prestamo_editar(request, prestamo_id):
    if request.method == 'POST':
        prestamo = get_object_or_404(Prestamos, pk=prestamo_id)
        form = PrestamosForm(request.POST, instance=prestamo)
        if form.is_valid():
            form.save()
            return redirect('prestamos')
    else:
        prestamo = get_object_or_404(Prestamos, pk=prestamo_id)
        clientes = Clientes.objects.all()
        form = PrestamosForm(instance=prestamo)
        context = {'prestamo': prestamo, 
                   'clientes':clientes, 
                   'form': form, 
                   'user_is_authenticated': request.user.is_authenticated
                   }
    return render(request, 'prestamos/prestamo_editar.html', context)

@login_required
def prestamo_crear(request):
    if request.method == 'POST':
        # Si el formulario se envía, procesa los datos
        form = PrestamosForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo préstamo en la base de datos
            return redirect('prestamos')  # Redirige a la lista de préstamos
    else:
        # Si es una solicitud GET, muestra el formulario vacío
        clientes = Clientes.objects.all()
        form = PrestamosForm()
        
    context={'form': form,
             'clientes': clientes,
             'user_is_authenticated': request.user.is_authenticated}
    # Renderiza la plantilla con el formulario
    return render(request, 'prestamos/prestamo_crear.html', context)

@login_required
def prestamo_borrar(request, prestamo_id):
    prestamo = Prestamos.objects.get(id=prestamo_id)
    if request.method == "POST":
        form = PasswordVerificationForm(request.user, request.POST)
        if form.is_valid():
            prestamo.delete()
            return redirect('prestamos')
        else:
            form = PasswordVerificationForm(request.user)
            
    form = PasswordVerificationForm(request.user)
    context = {
            'form': form, 
            'prestamo': prestamo,
            'error': 'Contraseña incorrecta',
            'user_is_authenticated': request.user.is_authenticated}
    return render(request, 'prestamos/prestamo_borrar.html', context)

@login_required
def prestamos_sin_pagar(request):
    if request.method == 'GET':  
        prestamos_sin_pagar = Prestamos.objects.filter(monto_pago__lt=F('monto_a_pagar'))
        context = {
            'prestamos_sin_pagar': prestamos_sin_pagar,
            'user_is_authenticated': request.user.is_authenticated
        }
        return render(request, 'prestamos/prestamos_sin_pagar.html', context)
    else:
        return HttpResponse("No hay préstamos sin pagar")
    
@login_required
def prestamos_pagados(request):
    if request.method == 'GET':  
        prestamos_pagados = Prestamos.objects.filter(monto_pago=F('monto_a_pagar'))
        context = {
            'prestamos_pagados': prestamos_pagados,
            'user_is_authenticated': request.user.is_authenticated
        }
        return render(request, 'prestamos/prestamos_pagados.html', context)
    else:
        return HttpResponse("No hay préstamos pagados")
    
# ---------- Pagos ----------
def obtener_montos_pagos_por_dia(request):
    # Obtener todos los pagos
    pagos = Pagos.objects.all()

    # Agrupar por fecha de pago y sumar los montos pagados
    montos_por_dia = pagos.values('fecha_pago').annotate(
        total_monto_pagado=Sum('monto')
    ).order_by('fecha_pago')

    # Preparar los datos para el JSON
    fechas = [pago['fecha_pago'].strftime('%Y-%m-%d') for pago in montos_por_dia]
    totales = [float(pago['total_monto_pagado']) for pago in montos_por_dia]

    # Devolver los datos en formato JSON
    return JsonResponse({
        'fechas': fechas,
        'totales': totales,
    })

@login_required
def pagos(request):
    clientes = Clientes.objects.all()
    pagos = Pagos.objects.all().order_by('-fecha_pago')

   # Obtener los pagos de un cliente específico (si se proporciona un cliente_id)
    pagos_cliente = None
    cliente = None
    cliente_id = request.GET.get('cliente_id')
    
    if cliente_id:
        cliente = get_object_or_404(Clientes, id=cliente_id)
        pagos_cliente = Pagos.objects.filter(cliente=cliente).order_by('-fecha_pago')

    # Si es una solicitud AJAX, devolver los pagos en formato JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cliente_id = request.GET.get('cliente_id')
        if cliente_id:
            cliente = get_object_or_404(Clientes, id=cliente_id)
            pagos_cliente = Pagos.objects.filter(cliente=cliente).order_by('-fecha_pago')
            
            # Convertir los pagos a un formato JSON
            pagos_data = []
            
            for pago in pagos_cliente:
                pagos_data.append({
                    'id': pago.id,
                    'fecha_pago': pago.fecha_pago.strftime('%Y-%m-%d'),
                    'moneda': str(pago.moneda),
                    'tipo_pago': str(pago.tipo_pago),
                    'referencia': pago.referencia,
                    'monto': str(pago.monto),
                    'prestamo': {
                        'id': pago.prestamo.id if pago.prestamo else None,
                        'cliente': {
                            'nombre': pago.prestamo.cliente.nombre if pago.prestamo else None,
                            'apellido': pago.prestamo.cliente.apellido if pago.prestamo else None
                        }
                    } if pago.prestamo else None,
                    'url_editar': reverse('pago_editar', args=[pago.id]),
                    'url_borrar': reverse('pago_borrar', args=[pago.id])
                })
            return JsonResponse({'pagos': pagos_data,})
        else:
            return JsonResponse({'error': 'Cliente no especificado'}, status=400)

    # Si no es una solicitud AJAX, renderizar la página normalmente
    context = {
        'pagos': pagos,
        'pagos_cliente': pagos_cliente,
        'clientes': clientes,
        'cliente': cliente,
        'user_is_authenticated': request.user.is_authenticated
    }
    return render(request, 'pagos/pagos.html', context)

@login_required
def pago_crear(request):
    if request.method == 'POST':
        form = PagosForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.save()
            return redirect('pagos')
        else:
            print(form.errors)
    else:
        form = PagosForm()
        
    clientes = Clientes.objects.all()
    tipos_pago = TipodePago.objects.all()
    monedas = Moneda.objects.all()
    prestamos = Prestamos.objects.all()
    tasa_cambio = TasaCambio.objects.filter(fecha=date.today()).order_by('-fecha').first().tasa_dia

    context = {
        'form':form,
        'clientes':clientes,
        'tipos_pago':tipos_pago,
        'monedas':monedas, 
        'prestamos':prestamos,
        'tasa_cambio': tasa_cambio,
        'user_is_authenticated': request.user.is_authenticated
    }
    return render(request, 'pagos/pago_crear.html', context)

def pago_editar(request, pago_id):
    pago = get_object_or_404(Pagos, pk=pago_id)
    if request.method == 'POST':
        form = PagosForm(request.POST, instance=pago)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.save()
            return redirect('pagos')
    else:
        form = PagosForm(instance=pago)
        clientes = Clientes.objects.all()
        tipos_pago = TipodePago.objects.all()
        monedas = Moneda.objects.all()
        prestamos = Prestamos.objects.all()
        
        context = {
            'form': form,
            'clientes': clientes,
            'tipos_pago': tipos_pago,
            'monedas': monedas,
            'prestamos': prestamos,
            'pago': pago,
            'user_is_authenticated': request.user.is_authenticated
        }
        return render(request, 'pagos/pago_editar.html', context) 
    
@login_required
def pago_borrar(request, pago_id):
    pago = Pagos.objects.get(id=pago_id)
    if request.method == "POST":
        form = PasswordVerificationForm(request.user, request.POST)
        if form.is_valid():
            pago.delete()
            return redirect('pagos')
        else:
            form = PasswordVerificationForm(request.user)
            
    form = PasswordVerificationForm(request.user)
    context = {
            'form': form, 
            'pago': pago,
            'error': 'Contraseña incorrecta',
            'user_is_authenticated': request.user.is_authenticated}
    return render(request, 'pagos/pago_borrar.html', context)

@login_required
def pago_detalles(request, pago_id):
    pago = get_object_or_404(Pagos, id=pago_id)
    
    context = {
        'pago': pago,
        'user_is_authenticated': request.user.is_authenticated
    }
    return render(request, 'pagos/pago_detalles.html', context)

# ---------- Tasas ----------
@login_required
def tasas(request):
    tasas = TasaCambio.objects.all()
    context = {
        'tasas': tasas,
        'user_is_authenticated': request.user.is_authenticated
    }
    return render(request, 'tasas/tasas.html', context)

@login_required
def tasa_crear(request):
    if request.method == "POST":
        form = TasaForm(request.POST)
        if form.is_valid():
            tasa = form.save(commit=False)
            tasa.save()
            return redirect('tasas')
        else:
            print(form.errors)
    
    else:
        form = TasaForm()
    context = {
        'tasas': tasas,
        'form': form,
        'user_is_authenticated': request.user.is_authenticated
    }
    return render(request, 'tasas/tasa_crear.html', context)

@login_required
def tasa_editar(request,tasa_id):
    if request.method == 'POST':
        tasa = get_object_or_404(TasaCambio, pk=tasa_id)
        form = TasaForm(request.POST, instance=tasa)
        if form.is_valid():
            form.save()
            return redirect('tasas')
    else:
        tasa = get_object_or_404(TasaCambio, pk=tasa_id)
        form = TasaForm(instance=tasa)
        context = {'form': form,
                   'tasa': tasa,
                   'user_is_authenticated': request.user.is_authenticated}
    return render(request, 'tasas/tasa_editar.html', context)

@login_required
def tasa_borrar(request, tasa_id):
    tasa = get_object_or_404(TasaCambio, id=tasa_id)
    if request.method == "POST":
        form = PasswordVerificationForm(request.user, request.POST)
        if form.is_valid():
            tasa.delete()
            return redirect('tasas')
        else:
            print(form.errors)  # Imprime los errores del formulario en la consola
    else:
        form = PasswordVerificationForm(request.user)
    
    context = {
        'form': form,
        'tasa': tasa,
        'user_is_authenticated': request.user.is_authenticated
    }
    return render(request, 'tasas/tasa_borrar.html', context)


# ---------- Auth ----------
def login(request):
    return render(request, 'signin.html')

@login_required
def signout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    else: 
        return HttpResponse("Method not allowed", status=405)