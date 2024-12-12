from django.shortcuts import render, redirect
from django.db.models import Count, Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse
from collections import defaultdict
import json
from .models import Prestamos
from datetime import timedelta, datetime
#from .forms import


# Create your views here.
@login_required
def home(request):
    context = {'mensaje':'error', 
            'prestamos': prestamos,
            'user_is_authenticated': request.user.is_authenticated}
    return render(request, 'home.html', context)

def obtener_prestamos_pagados_por_dia():
    # Obtener préstamos pagados agrupados por fecha
    prestamos_pagados = Prestamos.objects.filter(fecha_pago__isnull=False)
    prestamos_por_dia = prestamos_pagados.values('fecha_pago').annotate(total=Count('id')).order_by('fecha_pago')
    
    # Preparar datos para el gráfico
    fechas = [prestamo['fecha_pago'].strftime('%Y-%m-%d') for prestamo in prestamos_por_dia]
    totales = [prestamo['total'] for prestamo in prestamos_por_dia]

    
    print(fechas)
    return {
        'fechas': fechas,
        'totales': totales,
    }
    
def obtener_montos_pagados_por_dia():
    # Obtener montos pagados agrupados por fecha
    montos_pagados = Prestamos.objects.filter(fecha_pago__isnull=False)
    montos_por_dia = montos_pagados.values('fecha_pago').annotate(total=Sum('monto_pago')).order_by('fecha_pago')

    # Preparar datos para el gráfico
    fechas = [monto['fecha_pago'].strftime('%Y-%m-%d') for monto in montos_por_dia]
    totales = [float(monto['total']) for monto in montos_por_dia]

    return {
        'fechas': fechas,
        'totales': totales,
    }
    
@login_required
def prestamos(request):
    if request.method == 'GET':
        prestamos_pagados = Prestamos.objects.filter(fecha_pago__isnull=False)
        prestamos_sin_pagar = Prestamos.objects.filter(fecha_pago__isnull=True)
        
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

def login(request):
    return render(request, 'signin.html')

@login_required
def signout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    else:
        return HttpResponse("Method not allowed", status=405)