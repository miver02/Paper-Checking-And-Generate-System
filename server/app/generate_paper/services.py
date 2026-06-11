import json
import secrets
import string

from .models import GeneratedPaper
from ..tools.ai import AIServiceError


class AIService:
    TASK_ID_PREFIX = "gp-"
    TASK_ID_LENGTH = 48

    def __init__(self):
        from ..tools import AIToolClass, ai_prompt

        self.aitc = AIToolClass()
        self.ai_prompt = ai_prompt

    # 解析参考文献
    def _parse_reference_list(self, text: str):
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            return [text] if text else []

        if isinstance(parsed, list):
            return parsed

        if isinstance(parsed, dict):
            references = (
                parsed.get("references") or parsed.get("items") or parsed.get("data")
            )
            if isinstance(references, list):
                return references
            if isinstance(references, str) and references:
                return [references]

        if isinstance(parsed, str) and parsed:
            return [parsed]

        return [text] if text else []

    # 构建模板文本
    def _build_template_text(self, **templates):
        payload = {
            key: value for key, value in templates.items() if value not in (None, "")
        }
        if not payload:
            return ""
        return json.dumps(payload, ensure_ascii=False)

    def _parse_template_text(self, template_text: str):
        if not template_text:
            return {}

        try:
            parsed = json.loads(template_text)
        except json.JSONDecodeError:
            return {}

        return parsed if isinstance(parsed, dict) else {}

    def _generate_task_id(self):
        alphabet = string.ascii_letters + string.digits
        token = "".join(secrets.choice(alphabet) for _ in range(self.TASK_ID_LENGTH))
        return f"{self.TASK_ID_PREFIX}{token}"

    def _reserve_task_id(self):
        while True:
            task_id = self._generate_task_id()
            if not GeneratedPaper.objects.filter(task_id=task_id).exists():
                return task_id

    # 创建新的paper记录
    def _create_paper_record(
        self,
        user=None,
        requirements=None,
        title=None,
        template_text=None,
        status=None,
        task_id=None,
        failed_reason=None,
    ):
        paper = GeneratedPaper.objects.create(
            user=user if getattr(user, "is_authenticated", False) else None,
            title=title or "",
            requirements=requirements or "",
            template=template_text or "",
        )
        updates = {}
        if status is not None:
            updates["status"] = status
        if task_id is not None:
            updates["task_id"] = task_id
        if failed_reason is not None:
            updates["failed_reason"] = failed_reason
        if updates:
            self._persist_paper(paper, **updates)
        return paper

    # 更新1+个字段
    def _persist_paper(self, paper, status=None, **fields):
        for key, value in fields.items():
            if value is not None:
                setattr(paper, key, value)
        if status is not None:
            paper.status = status
        paper.save()
        return paper

    def _build_generation_result(self, paper):
        return {
            "id": paper.id,
            "task_id": paper.task_id,
            "status": paper.status,
            "title": paper.title,
            "requirements": paper.requirements,
            "template": paper.template,
            "abstract": paper.abstract,
            "key_words": paper.key_words,
            "abstract_en": paper.abstract_en,
            "key_words_en": paper.key_words_en,
            "content": paper.content,
            "summary": paper.summary,
            "thank_words": paper.thank_words,
            "literature": paper.literature,
            "failed_reason": paper.failed_reason or "",
            "created_at": paper.created_at,
            "updated_at": paper.updated_at,
            "completed_at": paper.completed_at,
        }

    def _mark_paper_failed(self, paper, reason, task_id=None):
        updates = {
            "failed_reason": reason,
        }
        if task_id is not None:
            updates["task_id"] = task_id
        self._persist_paper(paper, status="failed", **updates)
        return paper

    def generate_paper(
        self,
        requirements,
        title=None,
        template_abstract=None,
        template_body=None,
        template_summary=None,
        template_acknowledgement=None,
        template_reference=None,
        user=None,
    ):
        paper_title = title or ""
        task_id = self._reserve_task_id()
        template_text = self._build_template_text(
            abstract=template_abstract,
            body=template_body,
            summary=template_summary,
            acknowledgement=template_acknowledgement,
            reference=template_reference,
        )
        paper = self._create_paper_record(
            user=user,
            requirements=requirements,
            title=paper_title,
            template_text=template_text,
            status="queued",
            task_id=task_id,
        )

        from .tasks import generate_paper_task

        try:
            generate_paper_task.apply_async(
                args=(paper.id, getattr(user, "id", None)),
                task_id=task_id,
            )
        except Exception as exc:
            self._mark_paper_failed(paper, str(exc))
            raise AIServiceError(f"任务派发失败: {exc}") from exc

        return self._build_generation_result(paper)

    def get_paper_status(self, paper_id, user=None):
        paper = GeneratedPaper.objects.select_related("user").get(pk=paper_id)
        if user is not None and paper.user_id not in (None, getattr(user, "id", None)):
            raise PermissionError("无权访问该论文记录")
        return self._build_generation_result(paper)

    def execute_paper_generation(self, paper_id, user_id=None, task_id=None):
        paper = GeneratedPaper.objects.select_related("user").get(pk=paper_id)
        if user_id is not None and paper.user_id not in (None, user_id):
            raise PermissionError("无权生成该论文记录")

        if task_id is not None:
            self._persist_paper(paper, task_id=task_id)

        self._persist_paper(paper, status="generating", failed_reason="")

        template_payload = self._parse_template_text(paper.template)
        paper_title = paper.title or ""
        requirements = paper.requirements

        abstract_data = self.generate_abstract(
            requirements,
            title=paper_title,
            template_abstract=template_payload.get("abstract"),
            paper=paper,
        )
        body_data = self.generate_body(
            requirements,
            title=paper_title,
            template_body=template_payload.get("body"),
            paper=paper,
        )
        summary_data = self.generate_summary(
            requirements,
            title=paper_title,
            template_summary=template_payload.get("summary"),
            paper=paper,
        )
        acknowledgement_data = self.generate_acknowledgement(
            requirements,
            title=paper_title,
            template_acknowledgement=template_payload.get("acknowledgement"),
            paper=paper,
        )
        reference_data = self.generate_reference(
            requirements,
            title=paper_title,
            template_reference=template_payload.get("reference"),
            paper=paper,
        )

        self._persist_paper(
            paper,
            status="completed",
            failed_reason="",
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
            **self._build_generation_result(paper),
        }

    def generate_abstract(
        self,
        requirements,
        title=None,
        template_abstract=None,
        user=None,
        paper=None,
    ):
        if paper is None:
            paper = self._create_paper_record(
                user=user,
                title=title,
                requirements=requirements,
                template_text=self._build_template_text(abstract=template_abstract),
            )

        zh_abstract = self.aitc.get_ai_generate(
            self.ai_prompt.abstract_prompt(
                requirements, title=title, template_abstract=template_abstract
            )
        )

        en_abstract = self.aitc.get_ai_translation(zh_abstract)

        self._persist_paper(
            paper,
            status=paper.status if paper.status == "completed" else "generating",
            abstract=zh_abstract,
            abstract_en=en_abstract,
        )

        return {
            "id": paper.id,
            "status": paper.status,
            "abstract_zh": zh_abstract,
            "abstract_en": en_abstract,
        }

    def generate_body(
        self,
        requirements,
        title=None,
        template_body=None,
        user=None,
        paper=None,
    ):
        if paper is None:
            paper = self._create_paper_record(
                user=user,
                title=title,
                requirements=requirements,
                template_text=self._build_template_text(body=template_body),
            )

        content = self.aitc.get_ai_generate(
            self.ai_prompt.body_prompt(
                requirements, title=title, template_body=template_body
            )
        )

        self._persist_paper(
            paper,
            status=paper.status if paper.status == "completed" else "generating",
            content=content,
        )

        return {
            "id": paper.id,
            "status": paper.status,
            "content": content,
        }

    def generate_summary(
        self,
        requirements,
        title=None,
        template_summary=None,
        user=None,
        paper=None,
    ):
        if paper is None:
            paper = self._create_paper_record(
                user=user,
                title=title,
                requirements=requirements,
                template_text=self._build_template_text(summary=template_summary),
            )

        summary = self.aitc.get_ai_generate(
            self.ai_prompt.summary_prompt(
                requirements, title=title, template_summary=template_summary
            )
        )

        self._persist_paper(
            paper,
            status=paper.status if paper.status == "completed" else "generating",
            summary=summary,
        )

        return {
            "id": paper.id,
            "status": paper.status,
            "summary": summary,
        }

    def generate_acknowledgement(
        self,
        requirements,
        title=None,
        template_acknowledgement=None,
        user=None,
        paper=None,
    ):
        if paper is None:
            paper = self._create_paper_record(
                user=user,
                title=title,
                requirements=requirements,
                template_text=self._build_template_text(
                    acknowledgement=template_acknowledgement
                ),
            )

        thank_words = self.aitc.get_ai_generate(
            self.ai_prompt.acknowledgement_prompt(
                requirements,
                title=title,
                template_acknowledgement=template_acknowledgement,
            )
        )

        self._persist_paper(
            paper,
            status=paper.status if paper.status == "completed" else "generating",
            thank_words=thank_words,
        )

        return {
            "id": paper.id,
            "status": paper.status,
            "thank_words": thank_words,
        }

    def generate_reference(
        self,
        requirements,
        title=None,
        template_reference=None,
        user=None,
        paper=None,
    ):
        if paper is None:
            paper = self._create_paper_record(
                user=user,
                title=title,
                requirements=requirements,
                template_text=self._build_template_text(reference=template_reference),
            )

        literature_text = self.aitc.get_ai_generate(
            self.ai_prompt.reference_prompt(
                requirements, title=title, template_reference=template_reference
            )
        )

        literature = self._parse_reference_list(literature_text)
        self._persist_paper(
            paper,
            status=paper.status if paper.status == "completed" else "generating",
            literature=literature,
        )

        return {
            "id": paper.id,
            "status": paper.status,
            "literature": literature,
        }


aisv = AIService()
