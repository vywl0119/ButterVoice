from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'Boardapp'

urlpatterns = [
    path('co_detail/<str:id>', views.co_detail, name='co_detail'),
    path('cu_detail/<str:id>', views.cu_detail, name='cu_detail'),
    path('board/<str:type>', views.board, name='board'),
    path('search_board/<str:type>', views.search_board, name='search_board'),
    path('detail_category/<str:id>/<str:category>', views.detail_category, name='detail_category'),
    path('call_delete/<int:c_no>/<str:id>', views.call_delete, name='call_delete'),



    
]