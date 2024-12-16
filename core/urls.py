from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('prestamos/', views.prestamos, name='prestamos'),
    
    #clientes
    path('clientes/', views.clientes, name='clientes'),
    #path('clientes/<int:cliente_id>', views.cliente_detalles, name='cliente_detalles'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]