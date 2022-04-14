from django.shortcuts import render
from argon2 import PasswordHasher

def role(request):
    return render(request, 'Home/role.html')

def home(request):
    return render(request, 'Home/home.html')

def signin(request):
    return render(request, 'Home/signin.html')

def signup(request):
    type = "cu"
    if request.method == 'POST':
        type = request.POST.get('result')
    
    context = {
        'type': type,
    }
    return render(request, 'Home/signup.html', context)