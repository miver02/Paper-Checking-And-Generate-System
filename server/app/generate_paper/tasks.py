from celery import shared_task

from .models import GeneratedPaper
from .services import AIService
from ..tools.ai import AIServiceError


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def generate_paper_task(self, paper_id, user_id=None):
    """异步生成论文任务"""
    service = AIService()
    task_id = getattr(self.request, "id", None)

    try:
        return service.execute_paper_generation(
            paper_id,
            user_id=user_id,
            task_id=task_id,
        )
    except AIServiceError as exc:
        paper = GeneratedPaper.objects.filter(pk=paper_id).first()
        if paper is not None:
            if self.request.retries < self.max_retries:
                service._persist_paper(
                    paper,
                    status="generating",
                    task_id=task_id,
                    failed_reason=str(exc),
                )
            else:
                service._mark_paper_failed(paper, str(exc), task_id=task_id)

        if self.request.retries < self.max_retries:
            raise self.retry(exc=exc)
        raise
    except PermissionError as exc:
        paper = GeneratedPaper.objects.filter(pk=paper_id).first()
        if paper is not None:
            service._mark_paper_failed(paper, str(exc), task_id=task_id)
        raise
    except Exception as exc:
        paper = GeneratedPaper.objects.filter(pk=paper_id).first()
        if paper is not None:
            service._mark_paper_failed(paper, str(exc), task_id=task_id)
        raise
