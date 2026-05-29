from http import HTTPStatus

import dashscope
from django.conf import settings
from .ai_prompt import ai_prompt


class AIServiceError(RuntimeError):
    pass


class AIToolClass:
    def __init__(self):
        # self.ai_prompt = Prompt()
        pass

    def _get_value(self, obj, key, default=None):
        if obj is None:
            return default
        if isinstance(obj, dict):
            return obj.get(key, default)
        return getattr(obj, key, default)

    def _extract_text(self, response) -> str:
        if getattr(response, "status_code", None) != HTTPStatus.OK:
            raise AIServiceError(
                f"AI service failed: {self._get_value(response, 'code', '')} "
                f"{self._get_value(response, 'message', '')}".strip()
            )

        output = self._get_value(response, "output")
        if output is None:
            raise AIServiceError("AI service returned empty output")

        text = self._get_value(output, "text")
        if text:
            return str(text).strip()

        choices = self._get_value(output, "choices", []) or []
        if not choices:
            raise AIServiceError("AI service returned empty choices")

        message = self._get_value(choices[0], "message")
        if message is None:
            raise AIServiceError("AI service returned invalid message")

        content = self._get_value(message, "content")
        if isinstance(content, str) and content.strip():
            return content.strip()

        if isinstance(content, list) and content:
            first_item = content[0]
            if isinstance(first_item, dict):
                text = first_item.get("text")
                if text:
                    return str(text).strip()

        raise AIServiceError("AI service returned no text content")

    def get_ai_generate(self, messages: list) -> str:
        dashscope.base_http_api_url = settings.BASE_URL

        try:
            response = dashscope.MultiModalConversation.call(
                api_key=settings.ALIYUN_API_KEY,
                model=settings.ALIYUN_MODEL,
                messages=messages,
                temperature=0.2,
                top_p=0.9,
                presence_penalty=0,
                frequency_penalty=0.2
            )
        except Exception as exc:
            raise AIServiceError(f"AI service request failed: {exc}") from exc
        return self._extract_text(response)

    def get_ai_translation(self, text: str) -> str:
        dashscope.base_http_api_url = settings.BASE_URL

        try:
            response = dashscope.MultiModalConversation.call(
                api_key=settings.ALIYUN_API_KEY,
                model=settings.ALIYUN_MODEL,
                messages=ai_prompt.translation_prompt(text),
                temperature=0.1,
                top_p=0.9,
                # presence_penalty=0,
                # frequency_penalty=0.2
            )
        except Exception as exc:
            raise AIServiceError(f"AI service request failed: {exc}") from exc
        return self._extract_text(response)
