from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'Mainapp'

urlpatterns = [
    path('cu_call/<str:co_id>/<str:category>', views.cu_call, name = 'cu_call'),
    path('co_call/<int:c_no>', views.co_call, name = 'co_call'),
    path('ajax_method/', views.ajax_method, name='ajax_method'),

    path('cu_main/', views.cu_main, name = 'cu_main'),
    path('co_main/', views.co_main, name = 'co_main'),
    
    path('category/<str:category>', views.category, name = 'category'),

    path('call_update/', views.call_update, name = 'call_update'),

    path('star/<str:co_id>/<int:star>/<int:c_no>', views.star, name = 'star'),
    path('stars/<int:star>/<str:co_id>', views.stars, name = 'stars'),

    path('index/', views.index, name='index'),
    path('call/', views.call, name='call'),

    path('cu_call/upload_cu/', views.upload_cu, name='upload_cu'),
    path('upload_co/', views.upload_co, name='upload_co'),
]

