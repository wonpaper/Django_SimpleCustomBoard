from django.conf.urls import include
from django.urls import path

from . import views

urlpatterns = [
    path('', views.board_list, name='index'),
    path('list/', views.board_list, name='board_list'),
    path('detail/<int:no>/', views.board_detail, name='board_detail'),
    path('write/', views.board_write, name='board_write'),
    path('download/', views.file_download, name='file_download'),
    path('update/<int:no>/', views.board_update, name='board_update'),
    path('del/<int:no>/', views.board_delete, name='board_delete'),

]