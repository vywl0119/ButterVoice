from django.http import JsonResponse
from django.shortcuts import render, redirect
from Mainapp.models import counselor, customer
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt


def role(request):
    return render(request, 'Home/role.html')


def home(request):
    return render(request, 'Home/home.html')


def home_type(request, type):
    return render(request, 'Home/home.html', {'type': type})


def logout(request, type):
    if type == 'co':
        del request.session['co_id']
        del request.session['co_name']
        del request.session['co_type']
    else:
        del request.session['cu_id']
        del request.session['cu_name']
        del request.session['cu_type']

    return redirect('/Home/home/')


# 상담사와 고객 모두 따로 로그인했을때 각자의 세션이 남아있어야 해서 각 세션값 따로 생성


def signin(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        type = request.POST.get('type')
        print("id = ", id)
        print("pw = ", pw)
        print("type = ", type)

        if type == 'co':
            if counselor.objects.filter(co_id=id).exists():
                user = counselor.objects.get(co_id=id, pw=pw)
                print(user.pw)
                request.session['co_id'] = user.co_id
                request.session['co_name'] = user.name
                request.session['co_type'] = 'co'

                return redirect('Mainapp:co_main')
            else:
                messages.error(request, '아이디와 비밀번호를 확인해주세요.')
                return render(request, 'Home/signin.html')
        else:
            if customer.objects.filter(cu_id=id).exists():
                user = customer.objects.get(cu_id=id, pw=pw)
                request.session['cu_id'] = user.cu_id
                request.session['cu_name'] = user.name
                request.session['cu_type'] = 'cu'

                return redirect('Mainapp:cu_main')
            else:
                messages.error(request, '아이디와 비밀번호를 확인해주세요')
                return render(request, 'Home/signin.html')
    else:
        return render(request, 'Home/signin.html')


def signups(request, type):
    return render(request, 'Home/signup.html', {'type': type})


def signup(request):
    if request.method == 'POST':
        print('a')
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        profile = request.FILES.get('profile')

        print(type)
        print(id)

        if request.POST.get('type') == 'co':
            category = request.POST.get('category')
            comment = counselor.objects.create(co_id=id, pw=pw, category=category, name=name, phone=phone, profile=profile)
            comment.save()

            return redirect('/Home/signin')
        else:
            comment = customer.objects.create(cu_id=id, pw=pw, name=name, phone=phone, profile=profile)
            comment.save()

            return redirect('/Home/signin')


def mike(request):
    global num
    num = 0
    return render(request, 'Home/mike.html')


@csrf_exempt
def uploadFile(request):
    if request.method == "POST":
        uploaded = request.FILES['file']
        fs = FileSystemStorage(location='config/static/wav/')
        global num
        fs.save(f'test_{num}.wav', uploaded)
        num += 1

    return JsonResponse({"ok": "ok"})
