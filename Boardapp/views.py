from django.shortcuts import render, redirect
from Mainapp.models import counselor, customer, calling, point
from django.db.models import Q

# Create your views here.

# 상담사 상세페이지
def co_detail(request, id):
    
    # 상담사 정보
    user = counselor.objects.get(co_id=id)
   
    # 상담사가 담담한 모든 상담 list
    call_list = calling.objects.filter(co_id_id=id)

    # 상담사가 담당한 고객 이름 중복제거
    call_id = []
    for name in call_list:
        if name.cu_id_id not in call_id:
            call_id.append(name.cu_id_id)

    # 상담사가 담당한 중복제거한 고객 정보
    user_list = []
    for id in call_id:
        user_list.append(customer.objects.get(cu_id=id))

    # 상담사가 담당한 고객정보와 해당고객이 상담사와 상담한 정보 
    user_call = {}
    
    for i in user_list:
        user_call[customer.objects.get(cu_id=i.cu_id)] = calling.objects.filter(cu_id_id=i.cu_id, co_id_id=user.co_id)

    # 상담사가 담당한 모든 콜 수 와 상담사의 별점
    if call_list:
        call_cnt = len(call_list)
        total_star = point.objects.filter(co_id_id=user.co_id) 
        if total_star:
            star_cnt = len(total_star)
            sum_point = 0

            for i in total_star:
                sum_point += i.star           
            avg_point = round(sum_point/star_cnt,1)
        else:
            avg_point = 0
    else:
        avg_point = 0
        call_cnt = 0


    context = {
        'user':user,
        'call_list':call_list,
        'call_cnt':call_cnt,
        'avg_point':avg_point,
        'user_list':user_list,
        'user_call':user_call,
    }

    return render(request, 'Board/co_detail.html', context)

# 고객 상세페이지
def cu_detail(request, id):

    # 고객 정보
    user = customer.objects.get(cu_id=id)

    # 고객이 상담 리스트
    call_list = calling.objects.filter(cu_id_id=id)

    # 고객 상담 횟수
    call_cnt = len(call_list)

    # 고객이 상담한 상담사 정보
    profile_list = []
    for i in call_list:
        profile_list.append(counselor.objects.get(co_id=i.co_id_id).profile)

    # 고객이 상담한 상담사의 정보와 상담내용
    user_call = []
    for i, j in zip(profile_list, call_list):
        user_call.append([i,j])
        

    context = {
        'user':user,
        'call_list':call_list,
        'call_cnt':call_cnt,
        'id':id,
        'user_call':user_call,
    }

    return render(request, 'Board/cu_detail.html', context)

# 상담사와 고객 정보
def board(request, type):

    # 모든 상담사
    if type == 'co':
        users = counselor.objects.all()
    
    # 모든 고객
    else:
        users = customer.objects.all()

    return render(request, 'Board/board.html', {'users':users,'type':type})


# 이름, id 찾기
def search_board(request, type):

    if type == "co":
        total_board = counselor.objects.all()
        q = request.POST.get('q', "") 

        if q:
            users = total_board = total_board.filter(
                Q(co_id__icontains = q) | #상담사 id
                Q(name__icontains = q) #상담사 이름
            )           
            return render(request, 'Board/board.html', {'users' : users, 'type':type})

        else:
            return render(request, 'Boardapp:board')
    else:
        total_board = customer.objects.all()
        q = request.POST.get('q', "") 

        if q:
            users = total_board = total_board.filter(
                Q(cu_id__icontains = q) | #상담사 id
                Q(name__icontains = q) #상담사 이름
            )           
            return render(request, 'Board/board.html', {'users' : users, 'type':type})

        else:
            return render(request, 'Boardapp:board')

# 고객의 상담 카테고리별
def detail_category(request, id, category):

    # 고객 정보
    user = customer.objects.get(cu_id=id)
   
    # 해당 카테고리에 맞는 상담정보
    if category == 'ALL':
        call_list = calling.objects.filter(cu_id_id=id)
        call_cnt = len(call_list)
    if category == 'WIFI':
        call_list = calling.objects.filter(cu_id_id=id, category=category)
    if category == '핸드폰':
        call_list = calling.objects.filter(cu_id_id=id, category=category)
    if category == '가입':
        call_list = calling.objects.filter(cu_id_id=id, category=category)

    # 고객이 상담한 모든 상담 횟수
    all_call_list = calling.objects.filter(cu_id_id=id)
    call_cnt = len(all_call_list)
    

    # 고객이 상담한 상담사의 정보와 상담내용
    profile_list = []
    for i in call_list:
        profile_list.append(counselor.objects.get(co_id=i.co_id_id).profile)

    user_call = []
    for i, j in zip(profile_list, call_list):
        user_call.append([i,j])
    



    context = {
        'user':user,
        'call_list':call_list,
        'call_cnt':call_cnt,
        'id':id,
        'user_call':user_call,
    }

    return render(request, 'Board/cu_detail.html', context)

def call_delete(request, c_no, id):
        call = calling.objects.get(c_no=c_no)
        call.delete()
        return redirect( 'Boardapp:cu_detail', id=id)
    
