from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import UserRateThrottle

# 本地导入
from .services import LoginService
from .models import User
from .serializers.serializers import SuccessResponseSerializer, UserSerializer


class LoginRateThrottle(UserRateThrottle):
    rate = "5/m"
    scope = "login"


class CustomLoginView(ObtainAuthToken):
    username_field = "phone"
    permission_classes = [AllowAny]
    http_method_names = ["post"]  # 显式定义支持的 HTTP 方法
    throttle_classes = [LoginRateThrottle]

    def post(self, request, *args, **kwargs):
        # 1, 解析请求参数
        login_info = User(
            phone=request.data.get(self.username_field),
            password=request.data.get("password"),
        )

        # 2, 调用服务层处理逻辑
        user, token, created = LoginService.handle_login(login_info)

        # 3. 构造结构化响应
        serializer = SuccessResponseSerializer(
            {
                "code": status.HTTP_200_OK,
                "message": "登录成功",
                "data": {
                    "token": token.key,  # ✅ 字符串
                    "created": token.created,  # ✅ datetime
                    "user": UserSerializer(user).data,  # ✅ 序列化后的用户数据
                },
            }
        )

        # 4. 返回响应（传入serializer.data，而非实例）
        return Response(
            serializer.data, status=status.HTTP_200_OK  # 核心修复：使用.data属性
        )
