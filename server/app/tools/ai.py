import dashscope
from django.conf import settings

class AIToolClass:
    def get_ai_response(self, messages):
        dashscope.base_http_api_url = settings.BASE_URL

        response = dashscope.MultiModalConversation.call(
            api_key=settings.ALIYUN_API_KEY,
            model=settings.ALIYUN_MODEL,
            messages=messages
        )
        return response.output.choices[0].message.content[0]["text"]