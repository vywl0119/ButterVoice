from django.shortcuts import render

def role(request):
    return render(request, 'Home/role.html')

def home(request):
    return render(request, 'Home/home.html')

def signin(request):
    return render(request, 'Home/signin.html')

def signup(request):
    return render(request, 'Home/signup.html')