from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'Boardapp'

urlpatterns = [
    path('co_detail/<str:id>', views.co_detail, name='co_detail'),
    path('cu_detail/<str:id>', views.cu_detail, name='cu_detail'),
    path('board/<str:type>', views.board, name='board'),

    
]