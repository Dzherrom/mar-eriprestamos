from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
from .models import Prestamos
#from .forms import


# Create your views here.
def home(request):
    return render(request, 'home.html')

def prestamos(request):
    if request.method == 'GET':
        prestamos = Prestamos.objects.all()
        context = {'mensaje':'error', 'prestamos': prestamos}
        return render(request, 'prestamos/prestamos.html', context)
    