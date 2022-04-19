from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'Mainapp'

urlpatterns = [
    path('cu_call/', views.cu_call, name = 'cu_call'),
    path('co_call/', views.co_call, name = 'co_call'),
    path('cu_main/', views.cu_main, name = 'cu_main'),
    path('co_main/', views.co_main, name = 'co_main'),
    path('index/', views.index, name='index'),
    path('star/<int:star>', views.star, name = 'star'),
]