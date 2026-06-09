from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .serializers import (
    VersionedTokenObtainPairSerializer,
    VersionedTokenRefreshSerializer,
    VersionedTokenVerifySerializer,
)
from .views import LoginView, RegisterView, ProfileView, UploadAvatarView, LogoutView

urlpatterns = [
    path(
        "token/",
        TokenObtainPairView.as_view(
            serializer_class=VersionedTokenObtainPairSerializer
        ),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(serializer_class=VersionedTokenRefreshSerializer),
        name="token_refresh",
    ),
    path(
        "token/verify/",
        TokenVerifyView.as_view(serializer_class=VersionedTokenVerifySerializer),
        name="token_verify",
    ),
    path("login/", LoginView.as_view(), name="user_login"),
    path("register/", RegisterView.as_view(), name="user_register"),
    path("profile/", ProfileView.as_view(), name="user_profile"),
    path("avatar/", UploadAvatarView.as_view(), name="user_avatar"),
    path("logout/", LogoutView.as_view(), name="user_logout"),
]
