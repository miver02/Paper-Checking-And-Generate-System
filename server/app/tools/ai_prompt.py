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

    def _section_prompt(self, section_name: str, requirements, title=None, template=None) -> list:
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
                """
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
                        -> Return it unchanged

                        If NOT:
                        -> Rewrite a corrected version

                        Output ONLY the final corrected summary.
                    """
                },
                {
                    "role": "user",
                    "content": f"""
                        Requirements:
                        {requirements}

                        Template:
                        {template_abstract or ""}

                        Title:
                        {title or ""}

                        Summary:
                        {old_abstract}
                    """
                }
            ]

    def _refactor_text_prompt(self, section_name: str, requirements, old_content, title=None, template=None) -> list:
        return [
            {
                "role": "system",
                "content": f"""
                    You are a strict reviewer.

                    Check the {section_name} against:
                    1. Template structure compliance
                    2. Requirement satisfaction
                    3. Clarity and conciseness
                    4. No hallucination

                    If the {section_name} is PERFECT:
                    -> Return it unchanged

                    If NOT:
                    -> Rewrite a corrected version

                    Output ONLY the final corrected {section_name}.
                """
            },
            {
                "role": "user",
                "content": f"""
                    Requirements:
                    {requirements}

                    Template:
                    {template or ""}

                    Title:
                    {title or ""}

                    Original {section_name.capitalize()}:
                    {old_content}
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
                    {title or ""}

                    [Template]
                    {template_abstract or ""}

                    Generate the summary now.
                """
            }
        ]

    def body_prompt(self, requirements, title=None, template_body=None) -> list:
        return self._section_prompt("body", requirements, title=title, template=template_body)

    def body_refactor_prompt(self, requirements, old_body, title=None, template_body=None) -> list:
        return self._refactor_text_prompt("body", requirements, old_body, title=title, template=template_body)

    def summary_prompt(self, requirements, title=None, template_summary=None) -> list:
        return self._section_prompt("summary", requirements, title=title, template=template_summary)

    def summary_refactor_prompt(self, requirements, old_summary, title=None, template_summary=None) -> list:
        return self._refactor_text_prompt("summary", requirements, old_summary, title=title, template=template_summary)

    def acknowledgement_prompt(self, requirements, title=None, template_acknowledgement=None) -> list:
        return self._section_prompt(
            "acknowledgement",
            requirements,
            title=title,
            template=template_acknowledgement,
        )

    def acknowledgement_refactor_prompt(self, requirements, old_acknowledgement, title=None, template_acknowledgement=None) -> list:
        return self._refactor_text_prompt(
            "acknowledgement",
            requirements,
            old_acknowledgement,
            title=title,
            template=template_acknowledgement,
        )

    def reference_prompt(self, requirements, title=None, template_reference=None) -> list:
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
                """
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
                """
            }
        ]

    def reference_refactor_prompt(self, requirements, old_reference, title=None, template_reference=None) -> list:
        return [
            {
                "role": "system",
                "content": """
                    You are a strict reviewer.

                    Check the reference list against:
                    1. Template structure compliance
                    2. Requirement satisfaction
                    3. Clarity and conciseness
                    4. No hallucination

                    If the reference list is PERFECT:
                    -> Return it unchanged

                    If NOT:
                    -> Rewrite a corrected version

                    Strict Constraints:
                    - Output MUST be a valid JSON array
                    - Each item MUST be a single reference string
                    - Do NOT add explanations, markdown, or code fences

                    Output ONLY the final JSON array.
                """
            },
            {
                "role": "user",
                "content": f"""
                    Requirements:
                    {requirements}

                    Template:
                    {template_reference or ""}

                    Title:
                    {title or ""}

                    Original Reference List:
                    {old_reference}
                """
            }
        ]


ai_prompt = Prompt()
