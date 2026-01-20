from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import (
    JSONParser,
    FormParser,
    MultiPartParser,
)

# 本地导入
from .services import LoginService, RegisterService
from .serializers import (
    UserBaseInfoRes, UserRegisterReq, UserLoginReq, UpdateUserProfileReq
)
from app.security.throttles import (
    LoginIPThrottle, RegisterThrottle, UserThrottle, ApiThrottle,
    TokenThrottle,
)

from .utils import res_common


# 登录视图
class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]
    # throttle_classes = [LoginIPThrottle]

    def post(self, request):
        serializer = UserLoginReq(data=request.data)
        if not serializer.is_valid():
            err = serializer.errors
            if "phone" in err:
                return res_common.get_response400(err=err["phone"][0])
            return res_common.get_response400(str(err))

        try:
            result = LoginService.handle_login(**serializer.validated_data)
            data = {
                'access': result['access'],
                'refresh': result['refresh'],
                'user': UserBaseInfoRes(result['user']).data
            }
            return res_common.get_response200(message="登录成功", data=data)
        except Exception as e:
            return res_common.get_response400(err=str(e))


# 注册视图
class RegisterView(ObtainAuthToken):
    permission_classes = [AllowAny]
    # throttle_classes = [RegisterThrottle]

    def post(self, request):
        serializer = UserRegisterReq(data=request.data)
        if not serializer.is_valid():
            err = serializer.errors
            if "phone" in err:
                return res_common.get_response400(err=err["phone"][0])
            if "non_field_errors" in err:
                return res_common.get_response400(err=err["non_field_errors"][0])
            return res_common.get_response400(str(err))

        try:
            result = RegisterService.handle_register(
                **serializer.validated_data)
            data = {
                'access': result['access'],
                'refresh': result['refresh'],
                'user': UserBaseInfoRes(result['user']).data
            }
            return res_common.get_response200(message="注册成功", data=data)
        except Exception as e:
            return res_common.get_response400(err=str(e))


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    # throttle_classes = [UserThrottle, ApiThrottle, TokenThrottle]
    parser_classes = [
        JSONParser,
        FormParser,
        MultiPartParser,
    ]

    def get(self, request):
        try:
            user = request.user

            return res_common.get_response200("获取成功", UserBaseInfoRes(user, context={"request": request}).data)
        except Exception as e:
            return res_common.get_response400(err=str(e))

    def patch(self, request):
        """
        修改当前登录用户的个人信息（部分更新）
        """
        user = request.user

        serializer = UpdateUserProfileReq(
            instance=user,
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():
            err = serializer.errors
            if 'display_name' in err:
                return res_common.get_response400(err=err['display_name'][0])
            if 'avatar' in err:
                return res_common.get_response400(err=err['avatar'][0])
            return res_common.get_response400(str(err))
        try:
            # 删除旧头像（不是默认头像）
            if "avatar" in serializer.validated_data:
                if user.avatar and user.avatar.storage.exists(user.avatar.name):
                    user.avatar.delete(save=False)

            serializer.save()

            return res_common.get_response200("更新成功", UpdateUserProfileReq(user).data)
        except Exception as e:
            return res_common.get_response400(err=str(e))

class UploadAvatarView(APIView):
    permission_classes = [IsAuthenticated]
    # throttle_classes = [ApiThrottle]

    def post(self, request):
        user = request.user

        if user.avatar:
            user.avatar.delete(save=False)

        user.avatar = request.FILES['avatar']
        user.save(update_fields=['avatar'])
        return res_common.get_response200(data={"url": user.avatar.url})