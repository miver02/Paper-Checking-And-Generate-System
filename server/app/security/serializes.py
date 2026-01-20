from rest_framework import serializers

class SendVerifyCodeSerializer(serializers.Serializer):
    target = serializers.CharField()
    purpose = serializers.ChoiceField(choices=['change_phone', 'change_email'])
    channel = serializers.ChoiceField(choices=['sms', 'email'])

    def validate(self, attrs):
        if attrs['purpose'] == 'change_phone' and attrs['channel'] != 'sms':
            raise serializers.ValidationError('手机号必须使用短信验证码')
        if attrs['purpose'] == 'change_email' and attrs['channel'] != 'email':
            raise serializers.ValidationError('邮箱必须使用邮件验证码')
        return attrs

class ChangeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)


class ChangePhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=6)