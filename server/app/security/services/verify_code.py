import random
from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from django.conf import settings

from ..models import VerifyCode
from ..utils import send_sms, send_email


class VerifyCodeService:
    CODE_EXPIRE_MINUTES = 5
    RATE_LIMIT_SECONDS = 60

    @classmethod
    def _check_rate_limit(cls, *, target, purpose):
        recent = VerifyCode.objects.filter(
            target=target,
            purpose=purpose,
            created_at__gte=timezone.now() - timedelta(seconds=cls.RATE_LIMIT_SECONDS)
        ).exists()
        if recent:
            raise ValueError('请求过于频繁，请稍后再试')

    @classmethod
    def _generate_code(cls):
        return f"{random.randint(100000, 999999)}"

    @classmethod
    def send(cls, *, target, purpose, channel):
        """
        发送验证码（统一入口）
        """
        cls._check_rate_limit(target=target, purpose=purpose)

        code = cls._generate_code()

        vc = VerifyCode.objects.create(
            target=target,
            code=code,
            purpose=purpose,
            channel=channel,
            expires_at=timezone.now() + timedelta(minutes=cls.CODE_EXPIRE_MINUTES)
        )

        if channel == 'sms':
            send_sms(target, code)
        elif channel == 'email':
            send_email(target, code)
        else:
            raise ValueError('不支持的发送方式')

        return vc

    @classmethod
    @transaction.atomic
    def verify(cls, *, target, purpose, channel, code):
        """
        校验验证码（并自动标记已使用）
        """
        vc = (
            VerifyCode.objects
            .select_for_update()
            .filter(
                target=target,
                purpose=purpose,
                channel=channel,
                code=code,
                is_used=False
            )
            .order_by('-created_at')
            .first()
        )

        if not vc:
            raise ValueError('验证码错误')

        if vc.is_expired():
            raise ValueError('验证码已过期')

        vc.is_used = True
        vc.save(update_fields=['is_used'])

        return vc

    @staticmethod
    def can_change_phone(user):
        """判断手机号是否可以修改"""
        if not user.last_phone_change_at:
            return True

        delta = timezone.now() - user.last_phone_change_at
        return delta.total_seconds() >= settings.PHONE_CHANGE_INTERVAL