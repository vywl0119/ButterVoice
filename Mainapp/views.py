from django.shortcuts import render, redirect
from Mainapp.models import counselor, customer, calling, point
from datetime import date, datetime, timedelta

# Create your views here.

def cu_call(request, co_id, category):

    cu_id = request.session['cu_id']
    co_name = counselor.objects.get(co_id=co_id).name
    cu_name = customer.objects.get(cu_id=cu_id).name
 
    today = datetime.now().date()

    call = calling.objects.create(cu_id_id=cu_id, co_id_id=co_id, cu_name=cu_name, category = category, call_date = today)
    call.save()


    return render(request, 'Main/cu_call.html', {'co_name' : co_name, 'co_id':co_id, 'c_no':call.c_no})

def co_call(request, c_no):

    # 해당 전화 내역
    call = calling.objects.get(c_no=c_no)

    if call.current == '대기':
        call.current = '통화중'
        call.save()

    # 전화를 건 고객 id
    cu_id = calling.objects.get(c_no=c_no).cu_id_id

    # 상담사 id
    co_id = calling.objects.get(c_no=c_no).co_id_id

    # 전화를 건 고객 정보
    cu = customer.objects.get(cu_id = cu_id)

    # 전화를 건 고객 상담 정보
    cu_call = calling.objects.filter(cu_id_id=cu_id)

    
    context = {'cu':cu,
               'cu_call':cu_call,
               'call':call,
               
    }


    return render(request, 'Main/co_call.html', context)

def call_update(request):

    if request.method == 'POST':
        print('a')
   
        
        title = request.POST.get('title')
        content = request.POST.get('content')
        c_no = request.POST.get('c_no')

        call = calling.objects.get(c_no=c_no)
        call.title = title
        call.content = content
        call.save()
        
        
    return redirect('Mainapp:co_call', c_no=c_no )

def cu_main(request):

    total_co = counselor.objects.all()

    return render(request, 'Main/cu_main.html',{'total_co':total_co})

def co_main(request):

    co_id = request.session['co_id']

    wait_call = calling.objects.filter(co_id=co_id,current='대기')

    today = datetime.today()

    today_call = calling.objects.filter(call_date=today, co_id_id=co_id)
    today_call = len(today_call)

    if wait_call:
    
        first_call = wait_call[0]
        wait_call = wait_call[1:]
        call_len = len(wait_call)
    else:
        first_call = ""
        call_len = 0

    
    

    
    


    context = {'wait_call': wait_call,
                'first_call': first_call,
                'call_len':call_len,
                'today_call':today_call,
                } 

    return render(request, 'Main/co_main.html', context)


def star(request, co_id, star, c_no):

    if star == 6:
        call = calling.objects.get(c_no=c_no)
        call.current = '종료'
        call.save()


    print(co_id, star)

    return render(request, 'Main/star.html', {'star' : star, 'co_id':co_id, 'c_no':c_no})


def stars(request, star, co_id):

    print(co_id, star)
    print(type(star))
    print(type(co_id))

      
    star = point.objects.create(co_id_id=co_id, star=star)                                                                                                                                                                                                                                                                                                                                                                                                         
    star.save()


    return redirect('Mainapp:cu_main')


def index(request):
    return render(request, 'Main/index.html')
