from django.shortcuts import render
from Mainapp.models import counselor, customer, calling, point

# Create your views here.
def co_detail(request):
    return render(request, 'Board/co_detail.html')

def cu_detail(request):
    return render(request, 'Board/cu_detail.html')

def board(request, type):

    if type == 'co':
        users = counselor.objects.all()
    else:
        users = customer.objects.all()

    return render(request, 'Board/board.html', {'users':users,'type':type})

