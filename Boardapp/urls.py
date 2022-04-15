from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'Boardapp'

urlpatterns = [
    path('co_detail/', views.co_detail, name='co_detail'),
    path('cu_detail/', views.cu_detail, name='cu_detail'),
    path('board/', views.board, name='board'),
    path('co_board/', views.co_board, name='co_board'),
    path('cu_board/', views.cu_board,  name='cu_board'),
    
]