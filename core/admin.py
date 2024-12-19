from django.contrib import admin
from .models import Prestamos, Clientes, Pagos, Moneda, TipodePago

# Register your models here.

admin.site.register(Prestamos)
admin.site.register(Clientes)
admin.site.register(Pagos)
admin.site.register(TipodePago)
admin.site.register(Moneda)