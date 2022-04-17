from unicodedata import category
from django.shortcuts import render, redirect

from Mainapp.models import counselor, customer

def role(request):
    return render(request, 'Home/role.html')

def home(request):
    return render(request, 'Home/home.html')

def signin(request):

    if request.method == 'POST':

            id = request.POST.get('id')
            pw = request.POST.get('pw')
            type = request.POST.get('type')
            print("id = ",id )
            print("pw = ",pw )
            print("type = ",type )
        
            if type=='co':                
                user = counselor.objects.get(co_id = id, pw=pw)
                print(user.pw)

                context = {'user': user} 

                return render(request, 'Main/co_main.html',context)

                return redirect('Mainapp:co_main')


            else:
                user = customer.objects.filter(cu_id = id, pw=pw)   
                context = {'user': user}              
                return redirect('Mainapp:cu_main' )
    else:
        return render(request, 'Home/signin.html')


def signups(request, type):
    print(type)

    return render(request, 'Home/signup.html', {'type' : type})

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


