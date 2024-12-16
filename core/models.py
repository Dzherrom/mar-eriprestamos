from django.db import models

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
    
    def __str__(self):
        return self.nombre

class Prestamos(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField()
    fecha_pago = models.DateField(null=True, blank=True)
    monto_prestamo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monto_pago = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return f"Préstamo de {self.cliente} - Monto: {self.monto_prestamo}"
    
