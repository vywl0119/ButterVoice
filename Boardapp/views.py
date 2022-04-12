from django.shortcuts import render

# Create your views here.
def codetail(request):
    return render(request, 'Board/codetail.html')

def cudetail(request):
    return render(request, 'Board/cudetail.html')
