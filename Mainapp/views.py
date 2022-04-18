from django.shortcuts import render
from Mainapp.models import counselor, customer, colling, star
from datetime import date, datetime, timedelta

# Create your views here.

def cu_call(request, co_id, category):

    # if request.session['co_id']:
    #     del request.session['co_id']
    # else:
    
    cu_id = request.session['user_id']
    co_name = counselor.objects.get(co_id=co_id).name
 
    today = datetime.now().date()

    call = colling.objects.create(cu_id_id=cu_id, co_id_id=co_id, category = category, call_date = today)
    call.save()

    request.session['co_id'] = co_id


    return render(request, 'Main/cu_call.html', {'co_name' : co_name})

def co_call(request):
    return render(request, 'Main/co_call.html')

def cu_main(request):

    total_co = counselor.objects.all()

    return render(request, 'Main/cu_main.html',{'total_co':total_co})

def co_main(request):
    return render(request, 'Main/co_main.html')

def star(request, star):

    co_id = request.session['co_id'] 

    star = star.objects.create(co_id_id=co_id, star=star)                                                                                                                                                                                                                                                                                                                                                                                                           
    star.save()


    return render(request, 'Main/star.html', {'star' : star})
