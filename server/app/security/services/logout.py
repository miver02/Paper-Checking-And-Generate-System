from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings


class LogoutService:
    @staticmethod
    def invalidate_user_tokens(user):
        """
        通过提升用户 token_version 使当前用户的 JWT 立即失效。
        """
        with transaction.atomic():
            user_model = get_user_model()
            updated = user_model.objects.filter(pk=user.pk).update(
                token_version=F("token_version") + 1
            )
            if not updated:
                raise ValueError(f"User {user.pk} not found")

            user.refresh_from_db(fields=["token_version"])

    @staticmethod
    def revoke_refresh_token(refresh_token: str, user=None) -> None:
        """
        撤销当前设备的 refresh token，不影响其他设备。
        """
        with transaction.atomic():
            token = RefreshToken(refresh_token)
            if user is not None:
                token_user_id = token.payload.get(api_settings.USER_ID_CLAIM)
                if str(token_user_id) != str(getattr(user, api_settings.USER_ID_FIELD)):
                    raise ValueError("刷新令牌不属于当前用户")

            token.blacklist()
