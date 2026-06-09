from rest_framework_simplejwt.tokens import RefreshToken

TOKEN_VERSION_CLAIM = "token_version"


def get_user_token_version(user) -> int:
    return int(getattr(user, "token_version", 0) or 0)


def get_token_version_from_payload(payload) -> int:
    try:
        return int(payload.get(TOKEN_VERSION_CLAIM, 0) or 0)
    except (TypeError, ValueError):
        return 0


def apply_user_token_claims(token, user):
    token[TOKEN_VERSION_CLAIM] = get_user_token_version(user)
    return token


def build_user_token_pair(user) -> dict[str, str]:
    refresh = RefreshToken.for_user(user)
    apply_user_token_claims(refresh, user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
