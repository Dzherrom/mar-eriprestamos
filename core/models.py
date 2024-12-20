from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
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
    prestamos_pagados = models.IntegerField(default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.nombre

 
class Moneda(models.Model):
    MONEDA_CHOICES = [
        ('bolivares', 'Bolivares'),
        ('dolares', 'Dolares'),
    ]

    tipo_moneda = models.CharField(max_length=26, choices=MONEDA_CHOICES )

    def __str__(self):
        return self.tipo_moneda
    
class TipodePago(models.Model):
    tipo_pago = models.CharField(max_length=50, default='none')
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.tipo_pago
    
class Prestamos(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField()
    fecha_pago = models.DateField(null=True, blank=True)
    monto_prestamo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monto_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Monto total pagado
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Préstamo de {self.cliente} - Monto: {self.monto_prestamo}"
    @classmethod
    def contar_prestamos_activos(cls, cliente):
        return cls.objects.filter(cliente=cliente, fecha_pago__isnull=False).count()
    
    @classmethod    
    def contar_prestamos_pagados(cls, cliente):
        return cls.objects.filter(cliente=cliente, fecha_pago__isnull=True).count()
    
    @classmethod    
    def calcular_balance(cls, cliente):
        # Sumar el monto de los préstamos activos
        total_prestamos_activos = cls.objects.filter(cliente=cliente, fecha_pago__isnull=True).aggregate(Sum('monto_prestamo'))['monto_prestamo__sum'] or 0
        # Sumar el monto de los pagos realizados
        total_pagos_realizados = cls.objects.filter(cliente=cliente, fecha_pago__isnull=False).aggregate(Sum('monto_pago'))['monto_pago__sum'] or 0
        # Calcular el balance
        balance = total_prestamos_activos - total_pagos_realizados

        cliente.balance = balance
        cliente.save()
        
    @classmethod    
    def calcular_balance_total(cls, cliente):
        total_prestamos = Prestamos.objects.filter(cliente=cliente).aggregate(Sum('monto_prestamo'))['monto_prestamo__sum'] or 0
        cliente.total_prestamos = total_prestamos
        cliente.save()

class Pagos(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    fecha_pago = models.DateField()
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)
    tipo_pago = models.ForeignKey(TipodePago, on_delete=models.CASCADE)  # Inicialmente vacío
    referencia = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    prestamo = models.ForeignKey(Prestamos, on_delete=models.CASCADE, null=True, blank=True)  # Relación con Prestamos

    def __str__(self):
        return f"Pago de {self.monto} en {self.moneda} el {self.fecha_pago}"

    def save(self, *args, **kwargs):
        # Llamar al método save del modelo base
        super().save(*args, **kwargs)
        
        # Actualizar el monto pagado del préstamo asociado
        if self.prestamo:
            self.prestamo.monto_pago = (self.prestamo.monto_pago or 0) + self.monto
            self.prestamo.save()