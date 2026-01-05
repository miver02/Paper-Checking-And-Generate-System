from rest_framework import serializers

# 本地导入
from ..models import User

# 用户序列化器
class UserBaseInfoRes(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "phone", "email", "bio"]



