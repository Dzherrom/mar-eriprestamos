import re
from django import forms
from django.contrib.auth import authenticate
from django.core.files.base import File
from django.db.models.base import Model
from .models import Clientes, Prestamos, Pagos

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['nombre','apellido','genero',
                  'numero_telefono','numero_local',
                  'cedula','rif','tipo_persona',
                  'fecha_nacimiento','direccion_1',
                  'direccion_2','email_1','email_2']
        
    #funcion para validar el rif
    def clean_rif(self):
        rif = self.cleaned_data['rif']
        pattern = r'^[J|V|G|E]\d{10}$'
        if not re.match(pattern, rif):
            raise forms.ValidationError('El RIF debe tener el formato J1234567890')
        return rif
    
class PagosForm(forms.ModelForm):
    class Meta:
        model = Pagos
        fields = [
            'cliente', 'fecha_pago', 'moneda', 'tipo_pago', 'referencia', 
            'monto', 'prestamo', 'tasa_dia'
        ]
        
        widgets = {
        'fecha_prestamo': forms.DateInput(format='%Y/%m/%d', attrs={'type': 'date'}),
        'fecha_pago': forms.DateInput(format='%Y/%m/%d', attrs={'type': 'date'}),
        }

class PrestamosForm(forms.ModelForm):
    class Meta:
        model = Prestamos
        fields = [
            'cliente', 'fecha_prestamo', 'fecha_pago', 'monto_prestamo', 
            'monto_pago', 'monto_a_pagar', 'tasa_interes', 'pagado'
        ]
        
        widgets = {
                'fecha_prestamo': forms.DateInput(
                    format='%Y/%m/%d',
                    attrs={'type': 'date'}),
                'fecha_pago': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
            }
class PasswordVerificationForm(forms.Form):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordVerificationForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise forms.ValidationError('Contraseña incorrecta')
        return password