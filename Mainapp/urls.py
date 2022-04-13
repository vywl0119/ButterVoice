from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'Mainapp'

urlpatterns = [
    path('cu_call/', views.cu_call),
    path('co_call/', views.co_call),
    path('cu_main/', views.cu_main),
    path('co_main/', views.co_main),
    path('star/', views.star),
]