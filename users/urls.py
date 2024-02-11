from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('reset-password/', views.reset_password, name='reset_password'),

    path('', views.profiles, name='profiles'),
    path('profiles/<str:pk>/', views.user_profile, name='user-profile'),
]