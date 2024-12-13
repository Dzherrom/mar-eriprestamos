from django.contrib import admin
from .models import Prestamos, Clientes

# Register your models here.

admin.site.register(Prestamos)
admin.site.register(Clientes)