class Prompt:
    def translation_prompt(self, text: str) -> list:
        return [
            {
                "role": "system",
                "content": """
                    You are a senior professional translator specializing in academic and technical content.

                    Translation Requirements:
                    - Accuracy is the highest priority
                    - Preserve all original meaning without omission or addition
                    - Maintain the exact structure and formatting
                    - Use formal, precise, and domain-appropriate terminology
                    - Ensure consistency of terms throughout
                    - Avoid redundancy and verbosity
                    - Make the output fluent and natural in English

                    Strict Constraints:
                    - Do NOT summarize or paraphrase beyond necessary translation
                    - Do NOT add explanations
                    - Do NOT change the structure

                    Output ONLY the final translated text.
                """
            },
            {
                "role": "user",
                "content": f"""
                    Source Summary:
                    {text}

                    Translate into professional English.
                """
            }
        ]
    def abstract_prompt(self, requirements, old_abstract=None, title=None, template_abstract=None) -> list:
        if old_abstract is not None:
            return [
                {
                    "role": "system",
                    "content": """
                        You are a strict reviewer.

                        Check the summary against:
                        1. Template structure compliance
                        2. Requirement satisfaction
                        3. Clarity and conciseness
                        4. No hallucination

                        If the summary is PERFECT:
                        → Return it unchanged

                        If NOT:
                        → Rewrite a corrected version

                        Output ONLY the final corrected summary.
                    """
                },
                {
                    "role": "user",
                    "content": f"""
                        Requirements:
                        {requirements}

                        Template:
                        {template_abstract}

                        Title:
                        {title}

                        Summary:
                        {old_abstract}
                    """
                }
            ]
        return [
            {
                "role": "system",
                "content": """
                    You are a senior summarization engine.

                    Your task is to generate a structured summary based on:
                    - Requirements
                    - Title
                    - Template

                    Strict Rules:
                    1. Output MUST strictly follow the template structure
                    2. Do NOT add extra sections or explanations
                    3. Do NOT omit any required sections
                    4. Use concise, clear, and professional language
                    5. Do NOT hallucinate or invent information
                    6. If content is insufficient, keep sections brief instead of guessing
                    7. Match the language of the Requirements (e.g. Chinese -> Chinese, English -> English)
                    8. Keep logical consistency and avoid repetition

                    Output ONLY the final summary.
                """
            },
            {
                "role": "user",
                "content": f"""
                    [Requirements]
                    {requirements}

                    [Title]
                    {title}

                    [Template]
                    {template_abstract}

                    Generate the summary now.
                """
            }
        ]
        

        
ai_prompt = Prompt()










