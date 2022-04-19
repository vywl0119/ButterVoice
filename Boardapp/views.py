from django.shortcuts import render
from Mainapp.models import counselor, customer, calling, point

# Create your views here.

def co_detail(request, id):
    
    user = counselor.objects.get(co_id=id)
    call_list = calling.objects.filter(co_id_id=id)

    if call_list:

        call_cnt = len(call_list)

        total_star = point.objects.filter(co_id_id=id) 
        star_cnt = len(total_star)


        sum_point = 0
        for i in total_star:
            sum_point += i.star
        

        avg_point = round(sum_point/star_cnt,1)
    else:
        avg_point = 0
        call_cnt = 0


    context = {
        'user':user,
        'call_list':call_list,
        'call_cnt':call_cnt,
        'avg_point':avg_point,
    }

    return render(request, 'Board/co_detail.html', context)

def cu_detail(request, id):

    user = customer.objects.get(cu_id=id)
    call_list = calling.objects.filter(cu_id_id=id)
    call_cnt = len(call_list)

    context = {
        'user':user,
        'call_list':call_list,
        'call_cnt':call_cnt,
    }

    return render(request, 'Board/cu_detail.html', context)

def board(request, type):

    if type == 'co':
        users = counselor.objects.all()
    else:
        users = customer.objects.all()

    return render(request, 'Board/board.html', {'users':users,'type':type})

