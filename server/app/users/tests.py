from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from .tokens import build_user_token_pair


class LogoutApiTestCase(APITestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            phone="13800000000",
            password="test-password",
        )
        self.client = APIClient()

    def test_logout_revokes_only_current_refresh_token(self):
        current_pair = build_user_token_pair(self.user)
        other_pair = build_user_token_pair(self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {current_pair['access']}"
        )
        logout_response = self.client.post(
            reverse("user_logout"),
            {"refresh": current_pair["refresh"]},
            format="json",
        )

        self.assertEqual(logout_response.status_code, 200)
        self.assertEqual(logout_response.data["code"], 200)
        self.assertEqual(logout_response.data["message"], "当前设备已退出")

        profile_response = self.client.get(reverse("user_profile"))
        self.assertEqual(profile_response.status_code, 200)
        self.assertEqual(profile_response.data["code"], 200)

        current_refresh_response = self.client.post(
            reverse("token_refresh"),
            {"refresh": current_pair["refresh"]},
            format="json",
        )
        self.assertEqual(current_refresh_response.status_code, 401)

        other_refresh_response = self.client.post(
            reverse("token_refresh"),
            {"refresh": other_pair["refresh"]},
            format="json",
        )
        self.assertEqual(other_refresh_response.status_code, 200)
        self.assertIn("access", other_refresh_response.data)
