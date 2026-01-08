from rest_framework import serializers

# 本地导入
from ..models import User
from paper.settings import STATIC_URL


# 用户序列化器
class UserBaseInfoRes(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "phone", "email", "display_name", "avatar", "bio"]

    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return STATIC_URL + "avatars/default.png"

