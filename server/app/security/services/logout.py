from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

class LogoutService:
    def __init__(self):
        pass

    @staticmethod
    def blacklist_user_tokens(user):
        """
        将用户的JWT令牌加入黑名单
        """
        try:
            # 将该用户的所有活跃令牌加入黑名单
            for token in OutstandingToken.objects.filter(user=user):
                if not BlacklistedToken.objects.filter(token=token).exists():
                    BlacklistedToken.objects.create(token=token)
        except ImportError:
            # 如果没有安装jwt黑名单应用，则使用缓存方式
            from django.core.cache import cache
            cache_key = f"user_version_{user.id}"
            cache.set(cache_key, cache.get(cache_key, 0) + 1, timeout=None)
        except Exception as e:
            print(f"Error blacklisting tokens for user {user.id}: {str(e)}")