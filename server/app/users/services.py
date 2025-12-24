from django.db import IntegrityError
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.authtoken.models import Token

from .models import User
from .utils import logger


class LoginService:
    @staticmethod
    def validate_fields(fields: User) -> None:
        """
        校验登录必填字段（手机号/密码）是否为空
        :param login_field: 登录标识（手机号）
        :param password: 密码
        :raise ValidationError: 字段为空时抛出异常
        """
        if not fields.phone:
            raise ValidationError("手机号不能为空")
        if not fields.password:
            raise ValidationError("密码不能为空")

    @staticmethod
    def get_and_validate_user(fields: User) -> User:
        """
        获取用户并校验账号状态、密码正确性
        :param phone: 手机号
        :param password: 明文密码
        :return: 验证通过的User实例
        :raise AuthenticationFailed: 验证失败时抛出异常
        """
        try:
            user = User.objects.get(phone=fields.phone, is_deleted=False)
        except:
            logger.warning(f"登录失败：手机号{fields.phone}不存在或已删除")
            raise AuthenticationFailed(detail="手机号或密码错误", code=401)

        if not user.check_password(fields.password):
            logger.warning(f"登录失败：手机号{fields.phone}密码错误")
            raise AuthenticationFailed(detail="手机号或密码错误", code=401)
        
        if not user.is_active:
            logger.warning(f"登录失败：手机号{fields.phone}账号已被禁用")
            raise AuthenticationFailed(detail="账号已被禁用，请联系管理员", code=401)
        
        logger.info(f"用户 {fields} 登录验证通过")
        return user

    @staticmethod
    def generate_or_refresh_token(user: User) -> tuple[Token, bool]:
        """
        生成/刷新用户Token（先删后创，彻底解决唯一键冲突）
        :param user: User实例
        :return: (Token实例, 是否是新生成的Token)
        """
        # 标记是否是全新生成（非刷新）
        is_new = False
        
        try:
            # 第一步：尝试删除旧token（无论是否存在）
            Token.objects.filter(user=user).delete()
            logger.info(f"用户{user.phone}：旧Token已删除（若存在）")
            
            # 第二步：创建新token（原子操作，无冲突）
            token = Token.objects.create(user=user)
            is_new = True
            logger.info(f"用户{user.phone}：新Token已生成")
        
        except IntegrityError as e:
            # 极端并发场景兜底：删除后仍创建失败，直接获取现有token
            logger.warning(f"用户{user.phone}：创建新Token失败，兜底获取 - {str(e)}")
            token, is_new = Token.objects.get_or_create(user=user)
        
        except Exception as e:
            logger.error(f"用户{user.phone}：Token生成/刷新失败 - {str(e)}")
            raise  # 抛出异常，让视图层处理
        
        return token, is_new

    @classmethod
    def handle_login(cls, login_info: User) -> tuple[User, Token, bool]:
        """
        登录核心流程整合（对外提供的统一入口）
        :param phone: 手机号
        :param password: 密码
        :param ip: 登录IP（可选）
        :param user_agent: 登录设备（可选）
        :return: (用户实例, Token实例, 是否新生成Token)
        """
        # 1. 校验字段非空
        cls.validate_fields(login_info)
        # 2. 校验用户合法性
        user = cls.get_and_validate_user(login_info)
        # 3. 生成/刷新Token
        token, created = cls.generate_or_refresh_token(user)

        return user, token, created
