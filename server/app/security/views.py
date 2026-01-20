from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

# 本地导入
from app.users.models import User
from app.users import res_common
from .serializes import SendVerifyCodeSerializer, ChangeEmailSerializer, ChangePhoneSerializer
from .services import LogoutService, VerifyCodeService
from .utils import get_nowtime

class SendVerifyCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SendVerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            VerifyCodeService.send(
                target=serializer.validated_data['target'],
                purpose=serializer.validated_data['purpose'],
                channel=serializer.validated_data['channel'],
            )
        except ValueError as e:
            return res_common.get_response400(err=str(e))

        return res_common.get_response200(message='验证码已发送')


class ChangeEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangeEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        user = request.user

        if User.objects.filter(email=email).exists():
            return Response({'code': 400, 'message': '邮箱已被使用'})

        try:
            VerifyCodeService.verify(
                target=email,
                purpose='change_email',
                channel='email',
                code=code
            )
        except ValueError as e:
            return Response({'code': 400, 'message': str(e)})

        user.email = email
        user.save(update_fields=['email'])

        LogoutService.blacklist_user_tokens(user)

        return res_common.get_response200(message='邮箱修改成功')

class ChangePhoneView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']
        user = request.user

        # ⭐ 时间限制校验
        if not VerifyCodeService.can_change_phone(user):
            return res_common.get_response400(err='手机号修改过于频繁，请稍后再试')
            
        if User.objects.filter(phone=phone).exists():
            return res_common.get_response400(err='手机号已被使用')

        try:
            VerifyCodeService.verify(
                target=phone,
                purpose='change_phone',
                channel='sms',
                code=code
            )
        except ValueError as e:
            return res_common.get_response400(err=str(e))

        user.phone = phone
        user.last_phone_change_at = get_nowtime()
        user.save(update_fields=['phone', 'last_phone_change_at'])

        LogoutService.blacklist_user_tokens(user)

        return res_common.get_response200(message='手机号修改成功')