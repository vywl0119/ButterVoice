from django.shortcuts import render

# Create your views here.
def codetail(request):
    return render(request, 'Board/codetail.html')

def cudetail(request):
    return render(request, 'Board/cudetail.html')

def board(request):
    return render(request, 'Board/board.html')

def coboard(request):
    return render(request, 'Board/coboard.html')

def cuboard(request):
    return render(request, 'Board/cuboard.html')