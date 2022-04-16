from unicodedata import category
from django.shortcuts import render, redirect

from Mainapp.models import counselor, customer

def role(request):
    return render(request, 'Home/role.html')

def home(request):
    return render(request, 'Home/home.html')

def signin(request):
    return render(request, 'Home/signin.html')

def signups(request, type):
    print(type)
    context = {
        'type': type,
    }
    return render(request, 'Home/signup.html', context)

def signup(request):
    if request.method == 'POST':
        pw = request.POST.get('pw')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        profile = request.POST.get('profile')
        id = request.POST.get('id')

        if request.POST.get('type')=='co':
            category = request.POST.get('category')
            comment = counselor.objects.create(co_id=id, pw=pw, category = category, name=name, phone=phone, profile=profile)
            comment.save()

            return redirect('/Home/signin')

        else:
            comment = customer.objects.create(cu_id=id, pw=pw, name=name, phone=phone, profile=profile)
            comment.save()
            
            return redirect('/Home/signin')


