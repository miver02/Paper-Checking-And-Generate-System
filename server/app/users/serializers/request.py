from rest_framework import serializers
from django.core.validators import RegexValidator

# 本地导入
from ..models import User, PHONE_REGEX


# 用户反序列化器
class UserLoginReq(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=11, validators=[RegexValidator(PHONE_REGEX)])
    class Meta:
        model = User
        fields = ["phone", "password"]


class UserRegisterReq(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["phone", "password", "confirm_password"]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("两次密码不一致")
        
        # 清洗字段
        attrs.pop("confirm_password")
        return attrs