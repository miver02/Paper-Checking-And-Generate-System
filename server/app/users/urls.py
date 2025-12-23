from django.urls import path
from .views import CustomLoginView

urlpatterns = [
    # 登录接口
    path('api/login', CustomLoginView.as_view(), name='api_login'),  
]