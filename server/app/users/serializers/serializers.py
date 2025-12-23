from typing import Any, ClassVar, Dict, OrderedDict
from rest_framework import serializers, status

# 本地导入
from ..models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "phone", "bio"]


class SuccessResponseSerializer(serializers.Serializer):
    """
    通用成功响应序列化器
    支持自定义状态码、提示信息、响应数据，适配所有2xx成功场景
    """

    # 修复：直接声明DRF字段，无需手动加类型注解
    code = serializers.IntegerField(
        default=status.HTTP_200_OK,
        help_text="HTTP状态码，默认200（成功），201（创建成功）等",
    )
    message = serializers.CharField(
        default="操作成功", help_text="响应提示信息，可自定义（如：登录成功、创建成功）"
    )
    data = serializers.JSONField(
        required=False,
        allow_null=True,
        help_text="响应数据体，可选，支持任意JSON格式数据",
    )


class ErrorResponseSerializer(serializers.Serializer):
    """通用失败响应序列化器"""

    code = serializers.IntegerField(help_text="错误状态码")
    message = serializers.CharField(help_text="错误提示信息")
    errors = serializers.JSONField(
        required=False, allow_null=True, help_text="详细错误信息"
    )
