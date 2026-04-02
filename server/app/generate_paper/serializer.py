from rest_framework import serializers


class GenerateAbstractSerializer(serializers.Serializer):
    requirements = serializers.CharField(required=True)
    title = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    template_abstract = serializers.CharField(required=False, allow_null=True, allow_blank=True)

class RefactorAbstractSerializer(GenerateAbstractSerializer):
    old_abstract = serializers.CharField(required=True)