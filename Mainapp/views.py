from django.shortcuts import render, redirect
from Mainapp.models import counselor, customer, colling, point
from datetime import date, datetime, timedelta

# Create your views here.

def cu_call(request, co_id, category):

    cu_id = request.session['user_id']
    co_name = counselor.objects.get(co_id=co_id).name
 
    today = datetime.now().date()

    call = colling.objects.create(cu_id_id=cu_id, co_id_id=co_id, category = category, call_date = today)
    call.save()

    return render(request, 'Main/cu_call.html', {'co_name' : co_name, 'co_id':co_id})

def co_call(request):
    return render(request, 'Main/co_call.html')

def cu_main(request):

    total_co = counselor.objects.all()

    return render(request, 'Main/cu_main.html',{'total_co':total_co})

def co_main(request):
    return render(request, 'Main/co_main.html')

def star(request, co_id, star):

    print(co_id, star)

    # star = star.objects.create(co_id_id=co_id, star=star)                                                                                                                                                                                                                                                                                                                                                                                                           
    # star.save()


    return render(request, 'Main/star.html', {'star' : star, 'co_id':co_id})


def stars(request, star, co_id):

    print(co_id, star)
    print(type(star))
    print(type(co_id))

      
    star = point.objects.create(co_id_id=co_id, star=star)                                                                                                                                                                                                                                                                                                                                                                                                         
    star.save()


    return redirect('Mainapp:cu_main')
