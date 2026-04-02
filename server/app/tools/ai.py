import dashscope
from django.conf import settings
from .ai_prompt import ai_prompt

class AIToolClass:
    def __init__(self):
        # self.ai_prompt = Prompt()
        pass
    def get_ai_generate(self, messages: list) -> str:
        dashscope.base_http_api_url = settings.BASE_URL

        response = dashscope.MultiModalConversation.call(
            api_key=settings.ALIYUN_API_KEY,
            model=settings.ALIYUN_MODEL,
            messages=messages,
            temperature=0.2,
            top_p=0.9,
            presence_penalty=0,
            frequency_penalty=0.2
        )
        return response.output.choices[0].message.content[0]["text"]

    def get_ai_translation(self, text: list) -> str:
        dashscope.base_http_api_url = settings.BASE_URL

        response = dashscope.MultiModalConversation.call(
            api_key=settings.ALIYUN_API_KEY,
            model=settings.ALIYUN_MODEL,
            messages=ai_prompt.translation_prompt(text),
            temperature=0.1,
            top_p=0.9,
            # presence_penalty=0,
            # frequency_penalty=0.2
        )
        return response.output.choices[0].message.content[0]["text"]
