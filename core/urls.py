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
    path('api/prestamos/<int:id>/', prestamo_detalles_api, name='prestamo_detalles_api'),

    #clientes
    path('clientes/', views.clientes, name='clientes'),
    path('cliente/<int:cliente_id>', views.cliente_detalles, name='cliente_detalles'),
    path('cliente/crear', views.cliente_crear, name='cliente_crear'),
    path('cliente_borrar/<int:cliente_id>', views.cliente_borrar, name='cliente_borrar'),
    
    #pagos
    path('pagos/', views.pagos, name='pagos'),
]