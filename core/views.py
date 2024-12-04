from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
from .models import Prestamos
#from .forms import


# Create your views here.
@login_required
def home(request):
    context = {'mensaje':'error', 
            'prestamos': prestamos,
            'user_is_authenticated': request.user.is_authenticated}
    return render(request, 'home.html', context)

@login_required
def prestamos(request):
    if request.method == 'GET':
        prestamos = Prestamos.objects.all()
        context = {'mensaje':'error', 
                   'prestamos': prestamos,
                   'user_is_authenticated': request.user.is_authenticated}
        return render(request, 'prestamos/prestamos.html', context)

def login(request):
    return render(request, 'signin.html')

@login_required
def signout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    else:
        return HttpResponse("Method not allowed", status=405)