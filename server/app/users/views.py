from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import UserRateThrottle

# 本地导入
from .services import LoginService, RegisterService
from .serializers import (
    UserBaseInfoRes, UserRegisterReq, UserLoginReq
)

#  登录限流
class LoginRateThrottle(UserRateThrottle):
    rate = "5/m"
    scope = "login"


# 自定义登录视图
class CustomLoginView(ObtainAuthToken):
    username_field = "phone"
    permission_classes = [AllowAny]
    http_method_names = ["post"]  # 显式定义支持的 HTTP 方法
    throttle_classes = [LoginRateThrottle]

    def post(self, request, *args, **kwargs):
        deserializer = UserLoginReq(data=request.data)
        deserializer.is_valid(raise_exception=True)

        user, token,  created_if = LoginService.handle_login(**deserializer.validated_data)
        
        return Response(
            {
                "code": status.HTTP_200_OK,
                "message": "登录成功",
                "data": {
                    "token": token.key,
                    "created_if": created_if,
                    "user": UserBaseInfoRes(user).data,
                },
            },
            status=status.HTTP_200_OK
        )


# 自定义注册视图
class CustomRegisterView(ObtainAuthToken):
    username_field = "phone"
    permission_classes = [AllowAny]
    http_method_names = ["post"]  # 显式定义支持的 HTTP 方法
    throttle_classes = [LoginRateThrottle]

    def post(self, request, *args, **kwargs):
        deserializer = UserRegisterReq(data=request.data)
        deserializer.is_valid(raise_exception=True)

        user, token, created_if = RegisterService.handle_register(**deserializer.validated_data)

        return Response(
            {
                "code": status.HTTP_200_OK,
                "message": "登录成功",
                "data": {
                    "token": token.key,
                    "created": created_if,
                    "user": UserBaseInfoRes(user).data,
                },
            },
            status=status.HTTP_200_OK
        )
