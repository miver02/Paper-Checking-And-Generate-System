from django.urls import path
from .views import CustomLoginView, CustomRegisterView

urlpatterns = [
    path('api/login', CustomLoginView.as_view(), name='api_login'),  
    path('api/register', CustomRegisterView.as_view(), name='api_register'),  
]