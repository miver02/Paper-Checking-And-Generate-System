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
        生成/刷新用户Token（原子操作，避免并发问题）
        :param user: User实例
        :return: (Token实例, 是否是新生成的Token)
        """
        # get_or_create是数据库原子操作，避免并发生成多个Token
        token, created = Token.objects.get_or_create(user=user)

        # 如果Token已存在，刷新Token（旧Token失效，提升安全性）
        if not created:
            token.key = Token.generate_key()
            token.save(update_fields=["key"])
            logger.info(f"用户{user.phone}的Token已刷新")
        else:
            logger.info(f"用户{user.phone}的Token已生成（新）")

        return token, created

    @staticmethod
    def record_login_log(user: User, ip_addr: str = "", user_agent: str = "") -> None:
        """
        可选：记录用户登录日志（如需扩展登录日志功能，取消注释即可）
        :param user: User实例
        :param ip: 登录IP
        :param user_agent: 登录设备/浏览器信息
        """
        try:
            
            logger.info(f"用户{user.phone}登录日志已记录，IP：{ip}")
        except Exception as e:
            # 日志记录失败不影响登录流程，仅记录错误
            logger.error(f"用户{user.phone}登录日志记录失败：{str(e)}")

    @classmethod
    def handle_login(
        cls, login_info: User, ip_addr: str = "", user_agent: str = ""
    ) -> tuple[User, Token, bool]:
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
        # 4. 记录登录日志（可选）
        # cls.record_login_log(user, ip_addr, user_agent)

        return user, token, created
