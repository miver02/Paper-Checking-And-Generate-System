from django.urls import path
from .views import LoginView, RegisterView

urlpatterns = [
    path('user/login/', LoginView.as_view(), name='user_login'),  
    path('user/register/', RegisterView.as_view(), name='user_register'),  
]