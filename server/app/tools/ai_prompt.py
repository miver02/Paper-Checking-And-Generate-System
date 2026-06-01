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
                """,
            },
            {
                "role": "user",
                "content": f"""
                    Source Summary:
                    {text}

                    Translate into professional English.
                """,
            },
        ]

    def _section_prompt(
        self, section_name: str, requirements, title=None, template=None
    ) -> list:
        return [
            {
                "role": "system",
                "content": f"""
                    You are a senior academic writing engine.

                    Your task is to generate the {section_name} based on:
                    - Requirements
                    - Title
                    - Template

                    Strict Rules:
                    1. Output MUST strictly follow the template structure
                    2. Do NOT add extra sections or explanations
                    3. Do NOT omit any required sections
                    4. Use concise, clear, and professional language
                    5. Do NOT hallucinate or invent information
                    6. If content is insufficient, keep it brief instead of guessing
                    7. Match the language of the Requirements
                    8. Keep logical consistency and avoid repetition

                    Output ONLY the final {section_name}.
                """,
            },
            {
                "role": "user",
                "content": f"""
                    [Requirements]
                    {requirements}

                    [Title]
                    {title or ""}

                    [Template]
                    {template or ""}

                    Generate the {section_name} now.
                """,
            },
        ]

    def abstract_prompt(self, requirements, title=None, template_abstract=None) -> list:
        return self._section_prompt(
            "abstract", requirements, title=title, template=template_abstract
        )

    def body_prompt(self, requirements, title=None, template_body=None) -> list:
        return self._section_prompt(
            "body", requirements, title=title, template=template_body
        )

    def summary_prompt(self, requirements, title=None, template_summary=None) -> list:
        return self._section_prompt(
            "summary", requirements, title=title, template=template_summary
        )

    def acknowledgement_prompt(
        self, requirements, title=None, template_acknowledgement=None
    ) -> list:
        return self._section_prompt(
            "acknowledgement",
            requirements,
            title=title,
            template=template_acknowledgement,
        )

    def reference_prompt(
        self, requirements, title=None, template_reference=None
    ) -> list:
        return [
            {
                "role": "system",
                "content": """
                    You are a senior academic reference assistant.

                    Your task is to generate a reference list based on:
                    - Requirements
                    - Title
                    - Template

                    Strict Rules:
                    1. Output MUST be a valid JSON array
                    2. Each item MUST be a single reference string
                    3. Do NOT add explanations, markdown, or code fences
                    4. Do NOT invent unverifiable sources
                    5. If reliable references cannot be inferred, return an empty array

                    Output ONLY the final JSON array.
                """,
            },
            {
                "role": "user",
                "content": f"""
                    [Requirements]
                    {requirements}

                    [Title]
                    {title or ""}

                    [Template]
                    {template_reference or ""}

                    Generate the reference list now.
                """,
            },
        ]


ai_prompt = Prompt()
