from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import prestamo_detalles_api

urlpatterns = [
    path('', views.home, name='home'),
    
    #auth
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    #prestamos
    path('prestamos/', views.prestamos, name='prestamos'),
    path('prestamo_detalles/<int:prestamo_id>', views.prestamo_detalles, name='prestamo_detalles'),
    path('prestamo_editar/<int:prestamo_id>/', views.prestamo_editar, name='prestamo_editar'),
    path('prestamo/crear/', views.prestamo_crear, name='prestamo_crear'),
    path('prestamo_borrar/<int:prestamo_id>', views.prestamo_borrar, name='prestamo_borrar'),
    path('prestamos_pagados/', views.prestamos_pagados, name='prestamos_pagados'),
    path('prestamos_sin_pagar/', views.prestamos_sin_pagar, name='prestamos_sin_pagar'),
    
    path('api/prestamos/<int:id>/', prestamo_detalles_api, name='prestamo_detalles_api'),

    #clientes
    path('clientes/', views.clientes, name='clientes'),
    path('cliente/<int:cliente_id>', views.cliente_detalles, name='cliente_detalles'),
    path('cliente/crear', views.cliente_crear, name='cliente_crear'),
    path('cliente/editar_<int:cliente_id>', views.cliente_editar, name='cliente_editar'),
    path('cliente_borrar/<int:cliente_id>/', views.cliente_borrar, name='cliente_borrar'),
    
    #pagos
    path('pagos/', views.pagos, name='pagos'),
    path('pago_crear/', views.pago_crear, name='pago_crear'),
    path('pago_editar/<int:pago_id>', views.pago_editar, name='pago_editar'),
    path('pago_borrar/<int:pago_id>', views.pago_borrar, name='pago_borrar'),
    
    #tasas
    path('tasas/', views.tasas, name='tasas'),
    path('tasa_crear/', views.tasa_crear, name='tasa_crear'),
    path('tasa_editar/<int:tasa_id>', views.tasa_editar, name='tasa_editar'),
    path('tasa_borrar/<int:tasa_id>', views.tasa_borrar, name='tasa_borrar'),
    
    path('obtener-montos-pagos-por-dia/', views.obtener_montos_pagos_por_dia, name='obtener_montos_pagos_por_dia'),
    path('obtener-pagos-cliente/', views.pagos, name='obtener_pagos_cliente'),
    
]