from django.shortcuts import render

def role(request):
    return render(
        request, 'role.html'
    )
