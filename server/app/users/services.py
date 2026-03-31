from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

# 导入本地包
from .models import User
from ..tools import tc


# 登录服务
class LoginService:
    @staticmethod
    def handle_login(phone, password):
        # 验证用户
        user = authenticate(phone=phone, password=password)
        if not user:
            raise ValueError("用户名或密码错误")
        
        # 生成JWT token
        refresh = RefreshToken.for_user(user)
        access = AccessToken.for_user(user)

        user.last_login = tc.get_nowtime()
        user.save(update_fields=['last_login'])
        return {
            'refresh': str(refresh),
            'access': str(access),
            'user': user
        }


# 注册服务
class RegisterService:
    @staticmethod
    def handle_register(phone, password, **kwargs):
        # 检查用户是否已存在
        if User.objects.filter(phone=phone).exists():
            raise ValueError("用户已存在")
        
        # 创建用户
        user = User.users.create_user(
            phone=phone,
            password=password,
            last_login=tc.get_nowtime(),
            **kwargs
        )
        
        # 生成JWT token
        refresh = RefreshToken.for_user(user)
        access = AccessToken.for_user(user)
        
        return {
            'refresh': str(refresh),
            'access': str(access),
            'user': user
        }
