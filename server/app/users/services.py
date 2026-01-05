from django.db import IntegrityError
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.authtoken.models import Token

# 导入本地包
from .models import User
from app.log import logger


# 登录服务
class LoginService:
    @staticmethod
    def get_and_validate_user(phone: str, password: str) -> User:
        """
        校验用户是否存在、密码是否正确、账号状态是否合法
        """
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            logger.warning(f"登录失败：手机号{phone}不存在")
            raise AuthenticationFailed("手机号或密码错误", code=401)

        if not user.check_password(password):
            logger.warning(f"登录失败：手机号{phone}密码错误")
            raise AuthenticationFailed("手机号或密码错误", code=401)

        if not user.is_active:
            logger.warning(f"登录失败：手机号{phone}账号被禁用")
            raise AuthenticationFailed("账号已被禁用，请联系管理员", code=401)

        logger.info(f"用户 {phone} 登录验证通过")
        return user

    @staticmethod
    def generate_or_refresh_token(user: User) -> tuple[Token, bool]:
        """
        生成或刷新 Token（删除旧 Token 后创建新 Token）
        """
        try:
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            logger.info(f"用户{user.phone}：Token 已刷新")
            return token, True

        except IntegrityError as e:
            logger.warning(f"用户{user.phone}：Token 创建冲突，兜底获取 - {e}")
            token, created = Token.objects.get_or_create(user=user)
            return token, created

    @classmethod
    def handle_login(cls, *, phone: str, password: str) -> tuple[User, Token, bool]:
        """
        登录主流程（login_data 来自 serializer.validated_data）
        """
        user = cls.get_and_validate_user(phone, password)
        token, created = cls.generate_or_refresh_token(user)

        return user, token, created


# 注册服务
class RegisterService:
    @staticmethod
    def create_user(phone: str, password: str) -> User:
        """
        创建用户（校验手机号唯一性）
        """
        if User.objects.filter(phone=phone).exists():
            raise ValidationError("手机号已存在")

        user = User.users.create_user(
            phone=phone,
            password=password
        )
        return user

    @staticmethod
    def generate_token(user: User) -> tuple[Token, bool]:
        """
        生成新 Token（注册场景无需保留旧 Token）
        """
        try:
            token = Token.objects.create(user=user)
            logger.info(f"用户{user.phone}：Token 已生成")
            return token, True

        except IntegrityError:
            # 极端并发兜底
            token, created = Token.objects.get_or_create(user=user)
            return token, created

    @classmethod
    def handle_register(cls, *, phone: str, password: str) -> tuple[User, Token, bool]:
        """
        注册主流程（参数来自 serializer.validated_data）
        """
        user = cls.create_user(phone, password)
        token, created = cls.generate_token(user)
        return user, token, created
