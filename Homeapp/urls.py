from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'Homeapp'

urlpatterns = [
    path('role/', views.role),
    path('home/', views.home),
    path('signin/', views.signin),
    path('signup/', views.signup),
]