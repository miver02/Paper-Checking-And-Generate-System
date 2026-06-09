from django.contrib.auth import authenticate

# 导入本地包
from .models import User
from .tokens import build_user_token_pair
from ..tools import tc


# 登录服务
class LoginService:
    @staticmethod
    def handle_login(phone, password):
        # 验证用户
        user = authenticate(phone=phone, password=password)
        if not user:
            raise ValueError("用户名或密码错误")

        token_pair = build_user_token_pair(user)

        user.last_login = tc.get_nowtime()
        user.save(update_fields=['last_login'])
        return {
            'refresh': token_pair['refresh'],
            'access': token_pair['access'],
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

        token_pair = build_user_token_pair(user)
        
        return {
            'refresh': token_pair['refresh'],
            'access': token_pair['access'],
            'user': user
        }
