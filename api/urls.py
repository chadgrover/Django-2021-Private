from django.urls import path
from . import views

# Simple JWT Authentication Imports
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Simple JWT Authentication

    # The TokenObtainPairView view will return a new access and refresh token.
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # The TokenRefreshView view will return a new access token, if the refresh token is still valid.
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.get_routes),
    # If it's a function-based view, you can just pass the function name.
    path('projects/', views.get_projects),
    path('projects/<str:uuid>/', views.get_single_project),
    # Otherwise, you need to use the as_view() method for class-based views.

    path('projects/<str:uuid>/vote/', views.project_vote),
]