from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('list/', views.user_list, name='list'),
    path('<int:pk>/', views.profile, name='profile'),
    path('<int:pk>/edit/', views.profile_edit, name='profile_edit'),
    path('password/', views.UserPasswordChangeView.as_view(), name='password_change'),
]
