

class AIService:
    def __init__(self):
        pass

    def generate_paper(self, topic, requirements):
        pass
    def generate_abstract(self, text):
        return [
            {
            "role": "system",
            "content": "You are a helpful assistant. your name is miver"
            },
            {
            "role": "user",
            "content": text
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

aisv = AIService()