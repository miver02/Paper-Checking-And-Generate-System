from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

from .tokens import get_token_version_from_payload, get_user_token_version


class TokenVersionJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)

        token_version = get_token_version_from_payload(validated_token)
        if token_version != get_user_token_version(user):
            raise AuthenticationFailed(
                _("登录状态已失效，请重新登录"),
                code="token_version_mismatch",
            )

        return user
