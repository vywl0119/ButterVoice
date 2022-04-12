from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'Boardapp'

urlpatterns = [
    path('codetail/', views.codetail),
    path('cudetail/', views.cudetail),
    
]