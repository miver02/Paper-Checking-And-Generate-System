from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

# 本地导入
from .services import LoginService, RegisterService
from .serializers import (
    UserBaseInfoRes, UserRegisterReq, UserLoginReq
)
from app.security import LoginIPThrottle, RegisterThrottle



# 登录视图
class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]
    throttle_classes = [LoginIPThrottle]

    def post(self, request):
        serializer = UserLoginReq(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = LoginService.handle_login(**serializer.validated_data)
            return Response({
                'code': status.HTTP_200_OK,
                'message': '登录成功',
                'data': {
                    'access': result['access'],
                    'refresh': result['refresh'],
                    'user': UserBaseInfoRes(result['user']).data
                }
            })
        except Exception as e:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'message': str(e),
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)


# 注册视图
class RegisterView(ObtainAuthToken):
    permission_classes = [AllowAny]
    serializer_class = [UserRegisterReq]
    
    def post(self, request):
        serializer = UserRegisterReq(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            result = RegisterService.handle_register(**serializer.validated_data)
            return Response({
                'code': status.HTTP_200_OK,
                'message': '注册成功',
                'data': {
                    'access': result['access'],
                    'refresh': result['refresh'],
                    'user': UserBaseInfoRes(result['user']).data
                }
            })
        except Exception as e:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'message': str(e),
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)



class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "id": request.user.id,
            "username": request.user.username
        })