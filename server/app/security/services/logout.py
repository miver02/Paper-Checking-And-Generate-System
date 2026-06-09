from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F


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
