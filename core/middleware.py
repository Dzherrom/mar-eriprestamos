# filepath: /c:/Users/jerox/OneDrive/Documentos/Code/Python/mar-eriprestamos/core/middleware.py
from django.shortcuts import redirect
from datetime import date
from .models import TasaCambio

class TasaDiaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar si el usuario está autenticado
        if request.user.is_authenticated:
            # Excluir la URL de creación de tasa para evitar bucles de redirección
            if request.path not in ["/tasa_crear/", "/login/"]:
                # Verificar si existe una tasa_dia para la fecha actual
                tasa_dia = TasaCambio.objects.filter(fecha=date.today()).exists()
                if not tasa_dia:
                    return redirect('tasa_crear')

        response = self.get_response(request)
        return response