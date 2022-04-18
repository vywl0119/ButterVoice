from unicodedata import category
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserForm
from django.contrib import auth
from django.contrib.auth.models import User
from Mainapp.models import counselor, customer
from django.core.serializers.json import DjangoJSONEncoder
import json

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
                request.session['user'] = json.dumps(user, cls=DjangoJSONEncoder)  

              

                return redirect('Mainapp:co_main')


            else:
                user = customer.objects.get(cu_id = id, pw=pw)   
                   
                request.session['user'] = json.dumps(user, cls=DjangoJSONEncoder)  
 
                return render(request, 'Main/cu_main.html')
    else:
        return render(request, 'Home/signin.html')


def signups(request, type):

    return render(request, 'Home/signup.html', {'type' : type})

def signup(request):
    if request.method == 'POST':
        print('a')
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        profile = request.POST.get('profile')
        
        print(type)
        print(id)

        if request.POST.get('type')=='co':
            category = request.POST.get('category')
            comment = counselor.objects.create(co_id=id, pw=pw, category = category, name=name, phone=phone, profile=profile)
            comment.save()

            return redirect('/Home/signin')

        else:
            comment = customer.objects.create(cu_id=id, pw=pw, name=name, phone=phone, profile=profile)
            comment.save()
            
            return redirect('/Home/signin')

# def signup(request):
#     if request.method == 'POST':
#         if request.POST['pw'] == request.POST['pw_c']:
#             print('a')
#             user = User.objects.create_user(
#                                             username=request.POST['id'],
#                                             password=request.POST['pw'],
#                                             first_name =request.POST['name'],
#                                             phone=request.POST['phone'],
#                                             category =request.POST['category'],
#                                             profile =request.POST['profile'],
#                                             type =request.POST['type'],)
#             auth.login(request, user)
#             return redirect('/')
#         return render(request, 'signup.html')
#     return render(request, 'signup.html')



# def signup(request):
#     if request.method == "POST":
#         form = UserForm(request.POST)
#         print('test')
#         if form.is_valid():
#             print('a')
#             u = form.save(commit=False)
#             # 이메일
#             username = form.cleaned_data.get('username')
#             # 비밀번호
#             raw_password = form.cleaned_data.get('password1')
#             # 닉네임
#             first_name = form.cleaned_data.get('first_name')
#             # 고객/상담사
#             type = form.cleaned_data.get('type')
#             # 카테고리
#             category = form.cleaned_data.get('category')
#             # 핸드폰
#             phone = form.cleaned_data.get('phone')
#             # 프로필
#             profile_path = request.FILES.get('profile')
#             if profile_path:  
#                 name = profile_path.name
#                 with open('media/%s' % name, 'wb') as file:
#                     for chunk in profile_path.chunks():
#                         file.write(chunk)
#                 u.last_name = name
                
#             u.save()
#             print('b')
#             user = authenticate(username=username, password=raw_password, first_name=first_name, phone=phone, type=type, category=category,profile_path = profile_path)
#             print('c')
#             login(request, user)
#             return redirect('Mainapp:cu_main')
#     else:
#         form = UserForm()
#     return render(request, 'Home/signup.html', {'form': form})


