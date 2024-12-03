from django.db import models

# Create your models here.
class Clientes(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    numero_telefono = models.CharField(max_length=11)
    cedula = models.CharField(max_length=12)
    ciudad = models.CharField(max_length=150)
    
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
    