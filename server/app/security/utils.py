from django.utils import timezone

# security/utils.py
def ip_key(ip):
    return f"ip:{ip}"

def user_key(user_id):
    return f"user:{user_id}"

def api_key(path):
    return f"api:{path}"

def combo(*parts):
    return "rl:".join(parts)

def send_sms(phone, code):
    """
    对接短信平台
    """
    print(f'[SMS] {phone} -> {code}')
    # 实际调用阿里云 / 腾讯云 / Twilio


def send_email(email, code):
    """
    对接邮件服务
    """
    print(f'[EMAIL] {email} -> {code}')
    # Django send_mail / SES / SendGrid