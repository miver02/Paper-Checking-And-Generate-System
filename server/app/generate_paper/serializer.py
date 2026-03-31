from rest_framework import serializers

# 本地导入
from .models import GeneratedPaper

class GeneratedPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedPaper
        fields = "__all__"