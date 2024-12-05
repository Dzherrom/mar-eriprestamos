from django.shortcuts import render, redirect
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse
from .models import Prestamos
#from .forms import


# Create your views here.
@login_required
def home(request):
    context = {'mensaje':'error', 
            'prestamos': prestamos,
            'user_is_authenticated': request.user.is_authenticated}
    return render(request, 'home.html', context)

@login_required
def prestamos(request):
    if request.method == 'GET':
        prestamos = Prestamos.objects.all()
        prestamos_sin_pagar = [prestamo for prestamo in prestamos if prestamo.fecha_pago is None]
        prestamos_pagados = Prestamos.objects.filter(fecha_pago__isnull=False)
        
        # Agrupar préstamos pagados por fecha
        prestamos_por_dia = prestamos_pagados.values('fecha_pago').annotate(total=Count('id')).order_by('fecha_pago')
        # Preparar datos para el gráfico
        fechas = [prestamo['fecha_pago'].strftime('%Y-%m-%d') for prestamo in prestamos_por_dia]
        totales = [prestamo['total'] for prestamo in prestamos_por_dia]
        data_json = {
            'fechas': fechas,
            'totales': totales,
        }
        
        context = {'mensaje':'mensaje', 
                    'prestamos_sin_pagar': prestamos_sin_pagar,
                    'prestamos_pagados': prestamos_pagados,
                    'data_json': data_json,
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