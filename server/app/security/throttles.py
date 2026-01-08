# security/throttles.py
from rest_framework.throttling import BaseThrottle
from .services import RedisRateLimitService
from .utils import ip_key, user_key, api_key, combo


# 通用 Throttle 基类
class BaseServiceThrottle(BaseThrottle):
    rate = 60
    per = 60  # 秒

    def get_key(self, request):
        raise NotImplementedError

    def allow_request(self, request, view):
        key = self.get_key(request)
        RedisRateLimitService.check(combo(key), self.rate, self.per)
        return True


# IP 限流（匿名用户）
class IPThrottle(BaseServiceThrottle):
    rate = 100
    per = 60

    def get_key(self, request):
        ip = request.META.get("REMOTE_ADDR")
        return ip_key(ip)


# 用户限流（已登录）
class UserThrottle(BaseServiceThrottle):
    rate = 300
    per = 60

    def get_key(self, request):
        return user_key(request.user.id)


# API 限流（接口级）
class ApiThrottle(BaseServiceThrottle):
    rate = 50
    per = 60

    def get_key(self, request):
        return api_key(request.path)


# IP 限流（登录级）
class LoginIPThrottle(IPThrottle):
    rate = 10
    per = 600


# 注册 IP 限流
class RegisterThrottle(BaseServiceThrottle):
    rate = 5
    per = 600

    def get_key(self, request):
        ip = request.META.get("REMOTE_ADDR")
        return combo(
            ip_key(ip),
            api_key("register")
        )

# Token 维度限流（防 token 泄露）
class TokenThrottle(BaseServiceThrottle):
    rate = 100
    per = 60

    def get_key(self, request):
        return f"token:{request.auth}"