from django.shortcuts import render

# Create your views here.
def co_detail(request):
    return render(request, 'Board/co_detail.html')

def cu_detail(request):
    return render(request, 'Board/cu_detail.html')

def board(request):
    return render(request, 'Board/board.html')

def co_board(request):
    return render(request, 'Board/co_board.html')

def cu_board(request):
    return render(request, 'Board/cu_board.html')