from django.utils import timezone
from django.db import models

class VerifyCode(models.Model):
    PURPOSE_CHOICES = (
        ('change_phone', 'Change Phone'),
        ('change_email', 'Change Email'),
        # ('login', 'Login'),
        # ('register', 'Register'),
    )

    CHANNEL_CHOICES = (
        ('sms', 'SMS'),
        ('email', 'Email'),
    )

    target = models.CharField(max_length=255)  # phone or email
    code = models.CharField(max_length=6)

    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES)

    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
            verbose_name = "验证码记录"  
            verbose_name_plural = "验证码记录"
            ordering = ["-created_at"]  # 保留：按创建时间倒序
            db_table = "security_verify_code"  
    def is_expired(self):
        return timezone.now() > self.expires_at

