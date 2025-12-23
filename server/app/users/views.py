from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.views import ObtainAuthToken
from django_ratelimit.decorators import ratelimit
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

# 本地导入
from .services import LoginService
from .models import User
from .serializers.serializers import SuccessResponseSerializer


class CustomLoginView(ObtainAuthToken):
    username_field = "phone"
    permission_classes = [AllowAny]
    http_method_names = ['post']  # 显式定义支持的 HTTP 方法

    @ratelimit(key="ip", rate="5/m", method="POST", block=True)
    def post(self, request, *args, **kwargs):
        # 1, 解析请求参数
        login_info = User(
            phone=request.data.get(self.username_field),
            password=request.data.get("password"),
        )
        ip_addr = request.data.get("REMOTE_ADDR")
        user_agent = request.data.get("HTTP_USER_AGENT")

        # 2, 调用服务层处理逻辑
        user, token, created = LoginService.handle_login(
            login_info, ip_addr, user_agent
        )

        # 3. 构造结构化响应
        return Response(
            SuccessResponseSerializer(
                data={"token": token, "created": created, "user": user}
            ),
            status=status.HTTP_200_OK,
        )
