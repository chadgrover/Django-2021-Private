from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),
    path('', include('users.urls')),

    # Django REST Framework paths
    path('api/', include('api.urls')),

    # Password reset paths (Note: email backend must be configured in settings.py for this to work.)
    
    # Setting the template names allows us to use our own custom templates for the password reset process.
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='reset_password.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'), name='password_reset_complete'),
]

# Static files

# Creates a file path to the media folder in the project root directory.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Creates a file path to the static folder in the project root directory.
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Class based views need to be rendered using the as_view() method.