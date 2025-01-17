from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Sum, F
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse
from collections import defaultdict
from .models import Prestamos, Clientes, Pagos
from .forms import ClienteForm, PasswordVerificationForm, PrestamosForm
import json

@login_required
def home(request):
    context = {'mensaje':'error', 
            'prestamos': prestamos,
            'user_is_authenticated': request.user.is_authenticated}
    return render(request, 'home.html', context)

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

def cliente_detalles(request, cliente_id):
    if request.method == 'GET':
        clientes = Clientes.objects.all()
        cliente = Clientes.objects.get(id=cliente_id)
        print(cliente.nombre, cliente.apellido, cliente.cedula)
        prestamos = cliente.prestamos_set.all()
        pagos = Pagos.objects.filter(cliente=cliente)
        ultimo_pago = pagos.first()
        fecha_ultimo_pago = ultimo_pago.fecha_pago if ultimo_pago else None
        prestamos_activos = Prestamos.contar_prestamos_activos(cliente)
        prestamos_pagados = Prestamos.contar_prestamos_pagados(cliente)
        balance = Prestamos.calcular_balance_total(cliente)
        balance_total = Prestamos.suma_total_prestamos(cliente)
        tasa_interes_total = Prestamos.tasa_interes_total(cliente)
        form = ClienteForm(instance=cliente)
        
        for cliente in clientes:
            cliente.actualizar_balance()
        
        for prestamo in prestamos:
            Prestamos.calcular_balance_prestamo(prestamo)
        
        total_monto_a_pagar = sum(prestamo.monto_a_pagar for prestamo in prestamos)
        context = {'cliente': cliente,
                'clientes': clientes,
                'prestamos':prestamos,
                'pagos': pagos,
                'balance': balance,
                'balance_total': balance_total,
                'fecha_ultimo_pago': fecha_ultimo_pago,
                'prestamos_activos': prestamos_activos,
                'prestamos_pagados': prestamos_pagados,
                'total_monto_a_pagar': total_monto_a_pagar,
                'tasa_interes_total': tasa_interes_total,
                'form': form,
                'user_is_authenticated': request.user.is_authenticated}
        return render(request, 'clientes/cliente_detalles.html', context)
    
    else:
        try:
            clientes = get_object_or_404(Clientes, pk=cliente_id)
            form = ClienteForm(instance=clientes)
            if form.is_valid():
                form.save()
                print('form guarado correctamente')
                return redirect('home')
            
            else:
                print('error en try')
                return redirect('home')
        except:
            return render(request, 'cliente/cliente_detalles.html', context)
        
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
        prestamos_pagados = Prestamos.objects.filter(monto_pago=F('monto_a_pagar'))
        prestamos_sin_pagar = Prestamos.objects.filter(monto_pago__lt=F('monto_a_pagar'))
        
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
@login_required
def pagos(request):
    if request.method == 'GET':
        return render(request, 'Pagos/pagos.html')


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