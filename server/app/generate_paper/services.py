

class AIService:
    def __init__(self):
        from ..tools import AIToolClass, ai_prompt
        self.aitc = AIToolClass()
        self.ai_prompt = ai_prompt

    def generate_paper(self, topic, requirements):
        pass

    def generate_abstract(self, requirements, title=None, template_abstract=None):
        zh_abstract = self.aitc.get_ai_generate(self.ai_prompt.abstract_prompt(
            requirements, title=title, template_abstract=template_abstract))

        en_abstract = self.aitc.get_ai_translation(
            self.ai_prompt.translation_prompt(zh_abstract))

        # 写数据库

        return {
            "abstract_zh": zh_abstract,
            "abstract_en": en_abstract
        }

    def generate_body(self, text):

        return [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "你是谁？"
            }
        ]

    def generate_summary(self, text):
        return [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "你是谁？"
            }
        ]

    def generate_acknowledgement(self, text):
        return [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "你是谁？"
            }
        ]

    def generate_reference(self, text):
        return [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "你是谁？"
            }
        ]

    def refactor_abstract(self, requirements, old_abstract, title=None, template_abstract=None):
        zh_abstract = self.aitc.get_ai_generate(self.ai_prompt.abstract_prompt(
            requirements, old_abstract, title, template_abstract))

        en_abstract = self.aitc.get_ai_translation(
            self.ai_prompt.translation_prompt(zh_abstract))

        # 写入数据库
        
        return {
            "zh_abstract": zh_abstract,
            "en_abstract": en_abstract
        }
aisv = AIService()
