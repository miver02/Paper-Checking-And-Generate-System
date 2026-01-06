from django.urls import path
from .views import CustomLoginView, CustomRegisterView

urlpatterns = [
    path('user/login', CustomLoginView.as_view(), name='user_login'),  
    path('user/register', CustomRegisterView.as_view(), name='user_register'),  
]