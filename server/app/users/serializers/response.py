from rest_framework import serializers
from django.http import request

# 本地导入
from ..models import User
from paper.settings import STATIC_URL


# 用户序列化器
class UserBaseInfoRes(serializers.ModelSerializer):
    avatar = serializers.ImageField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "phone", "email", "display_name", "avatar", "bio"]

