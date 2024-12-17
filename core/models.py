from django.db import models
from django.db.models import Sum

# Create your models here.
class Clientes(models.Model):
    
    TIPO_PERSONA_CHOICES = [
        ('juridico', 'Jurídico'),
        ('natural', 'Natural'),
        ('extranjero', 'Extranjero'),
    ]
    
    GENERO_CHOICES = [
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
    ]
    
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES, default='masculino')
    numero_telefono = models.CharField(max_length=11)
    numero_local = models.CharField(max_length=11, default=None)
    cedula = models.CharField(max_length=12)
    rif = models.CharField(max_length=13, default='V1234567890')
    tipo_persona = models.CharField(max_length=10, choices=TIPO_PERSONA_CHOICES, default='natural')
    fecha_nacimiento = models.DateField(null=True, blank=False)
    direccion_1 = models.CharField(max_length=255, default='direccion')  # Mandatory field
    direccion_2 = models.CharField(max_length=255, null=True, blank=True)  # Optional field
    email_1 = models.EmailField(default=None)  # Mandatory field
    email_2 = models.EmailField(null=True, blank=True)  # Optional field
    prestamos_activos = models.IntegerField(default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    

    def __str__(self):
        return self.nombre

    def actualizar_prestamos_activos(self):
        self.prestamos_activos = self.prestamos.filter(fecha_pago__isnull=True).count()
        self.save()
    
    def actualizar_prestamos_activos(self):
        self.prestamos_activos = self.prestamos.filter(fecha_pago__isnull=True).count()
        self.save()
        
    def calcular_balance(self):
        # Sumar el monto de los préstamos activos
        total_prestamos_activos = self.prestamos.filter(fecha_pago__isnull=True).aggregate(Sum('monto_prestamo'))['monto_prestamo__sum'] or 0
        # Sumar el monto de los pagos realizados
        total_pagos_realizados = self.prestamos.filter(fecha_pago__isnull=False).aggregate(Sum('monto_pago'))['monto_pago__sum'] or 0
        # Calcular el balance
        self.balance = total_prestamos_activos - total_pagos_realizados
        self.save()
class Moneda(models.Model):
    MONEDA_DOLARES_CHOICES = [
        ('zelle', 'Zelle'),
        ('efectivo', 'Efectivo'),
        ('bofa', 'BOFA'),
        ('binance', 'Binance'),
    ]

    MONEDA_BOLIVARES_CHOICES = [
        ('transferencia_otros_bancos', 'Transferencia otros bancos'),
        ('transferencia', 'Transferencia'),
        ('pago_movil', 'Pago móvil'),
        ('efectivo', 'Efectivo'),
    ]

    tipo_moneda = models.CharField(max_length=26, choices=MONEDA_DOLARES_CHOICES + MONEDA_BOLIVARES_CHOICES)

    def __str__(self):
        return self.tipo_moneda

class Pagos(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    fecha_pago = models.DateField()
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)
    tipo_pago = models.CharField(max_length=50)  # Puedes usar choices aquí si deseas limitar las opciones
    referencia = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pago de {self.monto} en {self.moneda} el {self.fecha_pago}"
                
class Prestamos(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField()
    fecha_pago = models.DateField(null=True, blank=True)
    monto_prestamo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monto_pago = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return f"Préstamo de {self.cliente} - Monto: {self.monto_prestamo}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cliente.actualizar_prestamos_activos()
        self.cliente.actualizar_prestamos_pagados()
        self.cliente.calcular_balance()
        
