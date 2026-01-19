from django.urls import path
from .views import LoginView, RegisterView, ProfileView, UploadAvatarView

urlpatterns = [
    path('login/', LoginView.as_view(), name='user_login'),  
    path('register/', RegisterView.as_view(), name='user_register'),
    path('profile/', ProfileView.as_view(), name='user_profile'),
    path('avatar/', UploadAvatarView.as_view(), name='user_avatar')
]