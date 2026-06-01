import json

from django.db import transaction
from rest_framework.exceptions import NotFound, PermissionDenied

from .models import GeneratedPaper
from ..tools.ai import AIServiceError


class AIService:
    def __init__(self):
        from ..tools import AIToolClass, ai_prompt

        self.aitc = AIToolClass()
        self.ai_prompt = ai_prompt

    def _parse_reference_list(self, text: str):
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            return [text] if text else []

        if isinstance(parsed, list):
            return parsed

        if isinstance(parsed, dict):
            references = parsed.get("references") or parsed.get("items") or parsed.get("data")
            if isinstance(references, list):
                return references
            if isinstance(references, str) and references:
                return [references]

        if isinstance(parsed, str) and parsed:
            return [parsed]

        return [text] if text else []

    def _build_template_text(self, **templates):
        payload = {key: value for key, value in templates.items() if value not in (None, "")}
        if not payload:
            return ""
        return json.dumps(payload, ensure_ascii=False)

    def _resolve_paper(self, paper_id=None, user=None, topic=None, requirements=None, title=None, template_text=None):
        paper = None
        if paper_id is not None:
            try:
                paper = GeneratedPaper.objects.get(pk=paper_id)
            except GeneratedPaper.DoesNotExist as exc:
                raise NotFound("Paper record not found") from exc

        if paper is not None and user is not None and paper.user_id not in (None, user.id):
            raise PermissionDenied("Paper record does not belong to current user")

        if paper is None:
            return GeneratedPaper.objects.create(
                user=user if getattr(user, "is_authenticated", False) else None,
                title=title or topic or "",
                requirements=requirements or "",
                template=template_text or "",
            )

        updated = False
        if user is not None and paper.user_id is None:
            paper.user = user
            updated = True
        if title or topic:
            new_title = title or topic or ""
            if paper.title != new_title:
                paper.title = new_title
                updated = True
        if requirements and paper.requirements != requirements:
            paper.requirements = requirements
            updated = True
        if template_text and paper.template != template_text:
            paper.template = template_text
            updated = True
        if updated:
            paper.save()
        return paper

    def _persist_paper(self, paper, status=None, **fields):
        for key, value in fields.items():
            if value is not None:
                setattr(paper, key, value)
        if status is not None:
            paper.status = status
        paper.save()
        return paper

    def _refactor_text_section(
        self,
        *,
        requirements,
        old_content,
        prompt_builder,
        field_name,
        response_key,
        title=None,
        template_text=None,
        template_kwarg=None,
        paper_id=None,
        user=None,
        paper=None,
    ):
        with transaction.atomic():
            if paper is None:
                paper = self._resolve_paper(
                    paper_id=paper_id,
                    user=user,
                    title=title,
                    requirements=requirements,
                    template_text=template_text,
                )

            rewritten_content = self.aitc.get_ai_generate(
                prompt_builder(
                    requirements,
                    old_content,
                    title=title,
                    **({template_kwarg: template_text} if template_kwarg else {}),
                )
            )

            self._persist_paper(
                paper,
                status=paper.status if paper.status == "completed" else "generating",
                **{field_name: rewritten_content},
            )

            return {
                "paper_id": paper.id,
                "status": paper.status,
                response_key: rewritten_content,
            }

    def _refactor_reference_section(
        self,
        *,
        requirements,
        old_reference,
        title=None,
        template_text=None,
        paper_id=None,
        user=None,
        paper=None,
    ):
        with transaction.atomic():
            if paper is None:
                paper = self._resolve_paper(
                    paper_id=paper_id,
                    user=user,
                    title=title,
                    requirements=requirements,
                    template_text=template_text,
                )

            literature_text = self.aitc.get_ai_generate(
                self.ai_prompt.reference_refactor_prompt(
                    requirements,
                    old_reference,
                    title=title,
                    template_reference=template_text,
                )
            )
            literature = self._parse_reference_list(literature_text)

            self._persist_paper(
                paper,
                status=paper.status if paper.status == "completed" else "generating",
                literature=literature,
            )

            return {
                "paper_id": paper.id,
                "status": paper.status,
                "literature": literature,
            }

    def generate_paper(
        self,
        topic,
        requirements,
        title=None,
        paper_id=None,
        template_abstract=None,
        template_body=None,
        template_summary=None,
        template_acknowledgement=None,
        template_reference=None,
        user=None,
    ):
        with transaction.atomic():
            paper_title = title or topic
            template_text = self._build_template_text(
                abstract=template_abstract,
                body=template_body,
                summary=template_summary,
                acknowledgement=template_acknowledgement,
                reference=template_reference,
            )
            paper = self._resolve_paper(
                paper_id=paper_id,
                user=user,
                topic=topic,
                requirements=requirements,
                title=paper_title,
                template_text=template_text,
            )

            abstract_data = self.generate_abstract(
                requirements,
                title=paper_title,
                template_abstract=template_abstract,
                paper=paper,
            )
            body_data = self.generate_body(
                requirements,
                title=paper_title,
                template_body=template_body,
                paper=paper,
            )
            summary_data = self.generate_summary(
                requirements,
                title=paper_title,
                template_summary=template_summary,
                paper=paper,
            )
            acknowledgement_data = self.generate_acknowledgement(
                requirements,
                title=paper_title,
                template_acknowledgement=template_acknowledgement,
                paper=paper,
            )
            reference_data = self.generate_reference(
                requirements,
                title=paper_title,
                template_reference=template_reference,
                paper=paper,
            )

            self._persist_paper(
                paper,
                status="completed",
                abstract=abstract_data["abstract_zh"],
                abstract_en=abstract_data["abstract_en"],
                content=body_data["content"],
                summary=summary_data["summary"],
                thank_words=acknowledgement_data["thank_words"],
                literature=reference_data["literature"],
            )

            return {
                **abstract_data,
                **body_data,
                **summary_data,
                **acknowledgement_data,
                **reference_data,
                "paper_id": paper.id,
                "status": paper.status,
                "topic": topic,
                "title": paper_title,
                "requirements": requirements,
            }

    def generate_abstract(self, requirements, title=None, template_abstract=None, paper_id=None, user=None, paper=None):
        if paper is None:
            paper = self._resolve_paper(
                paper_id=paper_id,
                user=user,
                title=title,
                requirements=requirements,
                template_text=self._build_template_text(abstract=template_abstract),
            )

        zh_abstract = self.aitc.get_ai_generate(self.ai_prompt.abstract_prompt(
            requirements, title=title, template_abstract=template_abstract))

        en_abstract = self.aitc.get_ai_translation(zh_abstract)

        self._persist_paper(
            paper,
            status=paper.status if paper.status == "completed" else "generating",
            abstract=zh_abstract,
            abstract_en=en_abstract,
        )

        return {
            "paper_id": paper.id,
            "status": paper.status,
            "abstract_zh": zh_abstract,
            "abstract_en": en_abstract
        }

    def generate_body(self, requirements, title=None, template_body=None, paper_id=None, user=None, paper=None):
        if paper is None:
            paper = self._resolve_paper(
                paper_id=paper_id,
                user=user,
                title=title,
                requirements=requirements,
                template_text=self._build_template_text(body=template_body),
            )

        content = self.aitc.get_ai_generate(self.ai_prompt.body_prompt(
            requirements, title=title, template_body=template_body))

        self._persist_paper(
            paper,
            status=paper.status if paper.status == "completed" else "generating",
            content=content,
        )

        return {
            "paper_id": paper.id,
            "status": paper.status,
            "content": content,
        }

    def generate_summary(self, requirements, title=None, template_summary=None, paper_id=None, user=None, paper=None):
        if paper is None:
            paper = self._resolve_paper(
                paper_id=paper_id,
                user=user,
                title=title,
                requirements=requirements,
                template_text=self._build_template_text(summary=template_summary),
            )

        summary = self.aitc.get_ai_generate(self.ai_prompt.summary_prompt(
            requirements, title=title, template_summary=template_summary))

        self._persist_paper(
            paper,
            status=paper.status if paper.status == "completed" else "generating",
            summary=summary,
        )

        return {
            "paper_id": paper.id,
            "status": paper.status,
            "summary": summary,
        }

    def generate_acknowledgement(self, requirements, title=None, template_acknowledgement=None, paper_id=None, user=None, paper=None):
        if paper is None:
            paper = self._resolve_paper(
                paper_id=paper_id,
                user=user,
                title=title,
                requirements=requirements,
                template_text=self._build_template_text(acknowledgement=template_acknowledgement),
            )

        thank_words = self.aitc.get_ai_generate(self.ai_prompt.acknowledgement_prompt(
            requirements, title=title, template_acknowledgement=template_acknowledgement))

        self._persist_paper(
            paper,
            status=paper.status if paper.status == "completed" else "generating",
            thank_words=thank_words,
        )

        return {
            "paper_id": paper.id,
            "status": paper.status,
            "thank_words": thank_words,
        }

    def generate_reference(self, requirements, title=None, template_reference=None, paper_id=None, user=None, paper=None):
        if paper is None:
            paper = self._resolve_paper(
                paper_id=paper_id,
                user=user,
                title=title,
                requirements=requirements,
                template_text=self._build_template_text(reference=template_reference),
            )

        literature_text = self.aitc.get_ai_generate(self.ai_prompt.reference_prompt(
            requirements, title=title, template_reference=template_reference))

        literature = self._parse_reference_list(literature_text)
        self._persist_paper(
            paper,
            status=paper.status if paper.status == "completed" else "generating",
            literature=literature,
        )

        return {
            "paper_id": paper.id,
            "status": paper.status,
            "literature": literature,
        }

    def refactor_abstract(self, requirements, old_abstract, title=None, template_abstract=None, paper_id=None, user=None):
        with transaction.atomic():
            paper = self._resolve_paper(
                paper_id=paper_id,
                user=user,
                title=title,
                requirements=requirements,
                template_text=self._build_template_text(abstract=template_abstract),
            )

            zh_abstract = self.aitc.get_ai_generate(self.ai_prompt.abstract_prompt(
                requirements, old_abstract, title, template_abstract))

            en_abstract = self.aitc.get_ai_translation(zh_abstract)

            self._persist_paper(
                paper,
                status=paper.status if paper.status == "completed" else "generating",
                abstract=zh_abstract,
                abstract_en=en_abstract,
            )

            return {
                "paper_id": paper.id,
                "status": paper.status,
                "abstract_zh": zh_abstract,
                "abstract_en": en_abstract
            }

    def refactor_body(self, requirements, old_body, title=None, template_body=None, paper_id=None, user=None, paper=None):
        return self._refactor_text_section(
            requirements=requirements,
            old_content=old_body,
            prompt_builder=self.ai_prompt.body_refactor_prompt,
            field_name="content",
            response_key="content",
            title=title,
            template_text=template_body,
            template_kwarg="template_body",
            paper_id=paper_id,
            user=user,
            paper=paper,
        )

    def refactor_summary(self, requirements, old_summary, title=None, template_summary=None, paper_id=None, user=None, paper=None):
        return self._refactor_text_section(
            requirements=requirements,
            old_content=old_summary,
            prompt_builder=self.ai_prompt.summary_refactor_prompt,
            field_name="summary",
            response_key="summary",
            title=title,
            template_text=template_summary,
            template_kwarg="template_summary",
            paper_id=paper_id,
            user=user,
            paper=paper,
        )

    def refactor_acknowledgement(self, requirements, old_acknowledgement, title=None, template_acknowledgement=None, paper_id=None, user=None, paper=None):
        return self._refactor_text_section(
            requirements=requirements,
            old_content=old_acknowledgement,
            prompt_builder=self.ai_prompt.acknowledgement_refactor_prompt,
            field_name="thank_words",
            response_key="thank_words",
            title=title,
            template_text=template_acknowledgement,
            template_kwarg="template_acknowledgement",
            paper_id=paper_id,
            user=user,
            paper=paper,
        )

    def refactor_reference(self, requirements, old_reference, title=None, template_reference=None, paper_id=None, user=None, paper=None):
        return self._refactor_reference_section(
            requirements=requirements,
            old_reference=old_reference,
            title=title,
            template_text=template_reference,
            paper_id=paper_id,
            user=user,
            paper=paper,
        )


aisv = AIService()
