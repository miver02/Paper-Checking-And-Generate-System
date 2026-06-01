from rest_framework import serializers


class _BaseGenerateSerializer(serializers.Serializer):
    paper_id = serializers.IntegerField(required=False)
    requirements = serializers.CharField(required=True)
    title = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class GeneratePaperSerializer(_BaseGenerateSerializer):
    topic = serializers.CharField(required=True)
    template_abstract = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    template_body = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    template_summary = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    template_acknowledgement = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    template_reference = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class GenerateAbstractSerializer(_BaseGenerateSerializer):
    template_abstract = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class RefactorAbstractSerializer(GenerateAbstractSerializer):
    old_abstract = serializers.CharField(required=True)


class GenerateBodySerializer(_BaseGenerateSerializer):
    template_body = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class RefactorBodySerializer(GenerateBodySerializer):
    old_body = serializers.CharField(required=True)


class GenerateSummarySerializer(_BaseGenerateSerializer):
    template_summary = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class RefactorSummarySerializer(GenerateSummarySerializer):
    old_summary = serializers.CharField(required=True)


class GenerateAcknowledgementSerializer(_BaseGenerateSerializer):
    template_acknowledgement = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class RefactorAcknowledgementSerializer(GenerateAcknowledgementSerializer):
    old_acknowledgement = serializers.CharField(required=True)


class GenerateReferenceSerializer(_BaseGenerateSerializer):
    template_reference = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class RefactorReferenceSerializer(GenerateReferenceSerializer):
    old_reference = serializers.JSONField(required=True)
