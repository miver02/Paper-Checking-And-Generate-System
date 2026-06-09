from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import (
    TokenObtainSerializer,
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer,
)
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken

from ..tokens import (
    apply_user_token_claims,
    get_token_version_from_payload,
    get_user_token_version,
)


def _get_user_from_token_payload(payload):
    user_id = payload.get(api_settings.USER_ID_CLAIM)
    if not user_id:
        raise TokenError(_("Token contained no recognizable user identification"))

    user_model = get_user_model()
    try:
        return user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
    except user_model.DoesNotExist as exc:
        raise AuthenticationFailed(_("User not found"), code="user_not_found") from exc


def _ensure_token_version(token, user):
    token_version = get_token_version_from_payload(token)
    if token_version != get_user_token_version(user):
        raise TokenError(_("登录状态已失效，请重新登录"))


class VersionedTokenObtainPairSerializer(TokenObtainPairSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = TokenObtainSerializer.validate(self, attrs)

        refresh = self.get_token(self.user)
        apply_user_token_claims(refresh, self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class VersionedTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])
        user = _get_user_from_token_payload(refresh.payload)
        _ensure_token_version(refresh, user)

        data = {"access": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    refresh.blacklist()
                except AttributeError:
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()
            refresh.outstand()

            data["refresh"] = str(refresh)

        return data


class VersionedTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        token = UntypedToken(attrs["token"])

        if (
            api_settings.BLACKLIST_AFTER_ROTATION
            and "rest_framework_simplejwt.token_blacklist" in settings.INSTALLED_APPS
        ):
            jti = token.get(api_settings.JTI_CLAIM)
            if BlacklistedToken.objects.filter(token__jti=jti).exists():
                raise serializers.ValidationError(_("Token is blacklisted"))

        user = _get_user_from_token_payload(token.payload)
        _ensure_token_version(token, user)

        return {}
