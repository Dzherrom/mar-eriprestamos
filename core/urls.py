from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('prestamos/', views.prestamos, name='prestamos'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.signout, name='logout'),
]