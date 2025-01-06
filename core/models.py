from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
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
    ultimo_usuario_modificacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='clientes_modificados')
    fecha_ultima_modificacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre
    
    def actualizar_balance(self):
        """
        Actualiza el campo balance del cliente utilizando la función calcular_balance_total.
        """
        # Calcular el balance total del cliente
        balance_activo = Prestamos.calcular_balance_total(self)
        
        # Actualizar el campo balance del cliente
        self.balance = balance_activo
        
        # Guardar los cambios en la base de datos
        self.save()
 
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
    monto_a_pagar = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2)
    pagado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Préstamo de {self.cliente} - Monto: {self.monto_prestamo}"
    
    def save(self, *args, **kwargs):
        # Llamar al método save del modelo base
        super().save(*args, **kwargs)
        self.cliente.actualizar_balance()

        
    @classmethod
    def calcular_balance_total(cls, cliente):
        """
        Calcula el balance de un cliente como el total a pagar menos los pagos realizados.
        """
        # Obtener todos los préstamos activos del cliente
        prestamos_activos = cls.objects.filter(cliente=cliente, pagado=False)

        # Calcular el total a pagar y los pagos realizados
        total_a_pagar = sum(prestamo.monto_a_pagar for prestamo in prestamos_activos)
        pagos_realizados = sum(prestamo.monto_pago for prestamo in prestamos_activos)
        # Calcular el balance
        balance_activo = total_a_pagar - pagos_realizados
        return balance_activo


    @classmethod
    def calcular_balance_prestamo(cls, prestamo):
        """
        Calcula el balance de un cliente en un préstamo específico.
        Es decir, cuánto falta por pagar en ese préstamo.
        """
        # Verificar que el objeto prestamo sea válido
        if not isinstance(prestamo, cls):
            raise ValueError("Se esperaba un objeto de tipo Prestamos.")

        # Calcular el balance (total a pagar menos los pagos realizados)
        balance = prestamo.monto_a_pagar - prestamo.monto_pago
        return max(balance, 0)   # Asegurar que el balance no sea negativo
         
    @classmethod
    def total_a_pagar(cls, prestamo):
        """Calcula el total a pagar de un préstamo según la tasa de interés."""
        if prestamo.monto_prestamo and prestamo.tasa_interes:
            interes = (prestamo.monto_prestamo * prestamo.tasa_interes) / 100
            return prestamo.monto_prestamo + interes
        return 0
    
    @classmethod
    def suma_prestamos_activos(cls, cliente):
        """Calcula la suma total de los préstamos activos de un cliente."""
        return cls.objects.filter(cliente=cliente, fecha_pago__isnull=True).aggregate(Sum('monto_prestamo'))['monto_prestamo__sum'] or 0

    @classmethod
    def suma_total_prestamos(cls, cliente):
        """Calcula la suma total de todos los préstamos de un cliente,
        independientemente de si están activos o pagados."""
        return cls.objects.filter(cliente=cliente).aggregate(Sum('monto_prestamo'))['monto_prestamo__sum'] or 0
    
    @classmethod
    def suma_pagos_cliente(cls, cliente):
        """Calcula la suma total de los pagos de un cliente en sus préstamos activos."""
        return Pagos.objects.filter(cliente=cliente).aggregate(Sum('monto'))['monto__sum'] or 0

    @classmethod
    def tasa_interes_total(cls, cliente):
        """Calcula la suma total de la tasa de interés de los préstamos de un cliente."""
        return cls.objects.filter(cliente=cliente).aggregate(Sum('tasa_interes'))['tasa_interes__sum'] or 0

    @classmethod
    def contar_prestamos_pagados(cls, cliente):
        """Cuenta los préstamos que han sido pagados por un cliente."""
        return cls.objects.filter(cliente=cliente, pagado=True).count()

    @classmethod
    def contar_prestamos_activos(cls, cliente):
        """Cuenta los préstamos activos de un cliente."""
        return cls.objects.filter(cliente=cliente, pagado=False).count()

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
        self.cliente.actualizar_balance()
        
        # Actualizar el monto pagado del préstamo asociado
        if self.prestamo:
            self.prestamo.monto_pago = (self.prestamo.monto_pago or 0) + self.monto
            self.prestamo.save()