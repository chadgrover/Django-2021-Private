from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('create/', views.create_project, name='create-project'),
    path('update/<str:pk>/', views.update_project, name='update-project'),
    path('delete/<str:pk>/', views.delete_project, name='delete-project'),
    path('<str:pk>/', views.project, name='single-project'),
]