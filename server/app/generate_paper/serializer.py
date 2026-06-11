from rest_framework import serializers


class _BaseGenerateSerializer(serializers.Serializer):
    requirements = serializers.CharField(required=True)
    title = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class GeneratePaperSerializer(_BaseGenerateSerializer):
    template_abstract = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    template_body = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    template_summary = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    template_acknowledgement = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    template_reference = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class GenerateAbstractSerializer(_BaseGenerateSerializer):
    template_abstract = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class GenerateBodySerializer(_BaseGenerateSerializer):
    template_body = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class GenerateSummarySerializer(_BaseGenerateSerializer):
    template_summary = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class GenerateAcknowledgementSerializer(_BaseGenerateSerializer):
    template_acknowledgement = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class GenerateReferenceSerializer(_BaseGenerateSerializer):
    template_reference = serializers.CharField(required=False, allow_null=True, allow_blank=True)
