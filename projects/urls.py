from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='list'),
    path('project/list/', views.project_list, name='list_alt'),
    path('project/create/', views.project_create, name='create'),
    path('project/<int:pk>/', views.project_detail, name='detail'),
    path('project/<int:pk>/edit/', views.project_edit, name='edit'),
    path('project/<int:pk>/join/', views.project_join, name='join'),
    path('project/<int:pk>/complete/', views.project_complete, name='complete'),
    path('project/<int:pk>/favorite/', views.toggle_favorite, name='favorite'),
    path('favorites/', views.favorites_list, name='favorites'),
]
