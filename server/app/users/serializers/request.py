from rest_framework import serializers
from django.core.validators import RegexValidator

# 本地导入
from ..models import User, PHONE_REGEX


# 登录请求
class UserLoginReq(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=11, validators=[
                                  RegexValidator(PHONE_REGEX)])

    class Meta:
        model = User
        fields = ["phone", "password"]


# 注册请求
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


# 更新用户信息请求
class UpdateUserProfileReq(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["display_name", "avatar", "bio"]

    def validate_display_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("显示名太短")
        return value

    def validate_avatar(self, file):
        # 1. 类型校验
        if not file.content_type.startswith("image/"):
            raise serializers.ValidationError("只能上传图片文件")

        # 2. 大小限制（2MB）
        max_size = 2 * 1024 * 1024
        if file.size > max_size:
            raise serializers.ValidationError("头像大小不能超过 2MB")

        return file