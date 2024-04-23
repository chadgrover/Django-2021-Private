from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    # If it's a function-based view, you can just pass the function name.
    path('projects/', views.get_projects),
    path('projects/<str:uuid>/', views.get_single_project),
    # Otherwise, you need to use the as_view() method for class-based views.
]