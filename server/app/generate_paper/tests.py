from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient

from .models import GeneratedPaper
from .services import aisv
from ..tools.ai import AIServiceError


class AIServiceTestCase(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            phone="13800000000",
            password="test-password",
        )

    @patch("app.tools.ai.AIToolClass.get_ai_translation")
    @patch("app.tools.ai.AIToolClass.get_ai_generate")
    def test_generate_abstract_persists_paper(self, mock_generate, mock_translate):
        mock_generate.return_value = "中文摘要"
        mock_translate.return_value = "English Abstract"

        result = aisv.generate_abstract(
            requirements="围绕人工智能生成论文摘要",
            title="人工智能研究",
            template_abstract="模板摘要",
            user=self.user,
        )

        paper = GeneratedPaper.objects.get(pk=result["paper_id"])
        self.assertEqual(result["abstract_zh"], "中文摘要")
        self.assertEqual(result["abstract_en"], "English Abstract")
        self.assertEqual(paper.abstract, "中文摘要")
        self.assertEqual(paper.abstract_en, "English Abstract")
        self.assertEqual(paper.title, "人工智能研究")
        self.assertEqual(paper.user_id, self.user.id)

    @patch("app.tools.ai.AIToolClass.get_ai_translation")
    @patch("app.tools.ai.AIToolClass.get_ai_generate")
    def test_generate_paper_updates_generated_paper(self, mock_generate, mock_translate):
        mock_generate.side_effect = [
            "中文摘要",
            "论文正文",
            "论文总结",
            "致谢内容",
            '["Ref 1", "Ref 2"]',
        ]
        mock_translate.return_value = "English Abstract"

        result = aisv.generate_paper(
            topic="人工智能",
            requirements="写一篇人工智能论文",
            title="人工智能论文",
            template_abstract="摘要模板",
            template_body="正文模板",
            template_summary="总结模板",
            template_acknowledgement="致谢模板",
            template_reference="参考文献模板",
            user=self.user,
        )

        paper = GeneratedPaper.objects.get(pk=result["paper_id"])
        self.assertEqual(paper.status, "completed")
        self.assertEqual(paper.abstract, "中文摘要")
        self.assertEqual(paper.abstract_en, "English Abstract")
        self.assertEqual(paper.content, "论文正文")
        self.assertEqual(paper.summary, "论文总结")
        self.assertEqual(paper.thank_words, "致谢内容")
        self.assertEqual(paper.literature, ["Ref 1", "Ref 2"])
        self.assertEqual(result["status"], "completed")

    @patch("app.tools.ai.AIToolClass.get_ai_translation")
    @patch("app.tools.ai.AIToolClass.get_ai_generate")
    def test_generate_paper_rolls_back_on_failure(self, mock_generate, mock_translate):
        mock_generate.side_effect = [
            "中文摘要",
            AIServiceError("AI service failed"),
        ]
        mock_translate.return_value = "English Abstract"

        with self.assertRaises(AIServiceError):
            aisv.generate_paper(
                topic="人工智能",
                requirements="写一篇人工智能论文",
                title="人工智能论文",
                template_abstract="摘要模板",
                template_body="正文模板",
                template_summary="总结模板",
                template_acknowledgement="致谢模板",
                template_reference="参考文献模板",
                user=self.user,
            )

        self.assertEqual(GeneratedPaper.objects.count(), 0)

    @patch("app.tools.ai.AIToolClass.get_ai_translation")
    @patch("app.tools.ai.AIToolClass.get_ai_generate")
    def test_refactor_abstract_rolls_back_on_failure(self, mock_generate, mock_translate):
        paper = GeneratedPaper.objects.create(
            user=self.user,
            title="旧题目",
            requirements="旧要求",
            template="旧模板",
            abstract="旧摘要",
            abstract_en="Old Abstract",
        )

        mock_generate.return_value = "新中文摘要"
        mock_translate.side_effect = AIServiceError("AI service failed")

        with self.assertRaises(AIServiceError):
            aisv.refactor_abstract(
                requirements="新要求",
                old_abstract="旧摘要",
                title="新题目",
                template_abstract="新模板",
                paper_id=paper.id,
                user=self.user,
            )

        paper.refresh_from_db()
        self.assertEqual(GeneratedPaper.objects.count(), 1)
        self.assertEqual(paper.title, "旧题目")
        self.assertEqual(paper.requirements, "旧要求")
        self.assertEqual(paper.template, "旧模板")
        self.assertEqual(paper.abstract, "旧摘要")
        self.assertEqual(paper.abstract_en, "Old Abstract")

    @patch("app.tools.ai.AIToolClass.get_ai_generate")
    def test_refactor_body_updates_generated_paper(self, mock_generate):
        paper = GeneratedPaper.objects.create(
            user=self.user,
            title="旧题目",
            requirements="旧要求",
            template="旧模板",
            content="旧正文",
        )
        mock_generate.return_value = "新正文"

        result = aisv.refactor_body(
            requirements="新要求",
            old_body="旧正文",
            title="新题目",
            template_body="新模板",
            paper_id=paper.id,
            user=self.user,
        )

        paper.refresh_from_db()
        self.assertEqual(result["content"], "新正文")
        self.assertEqual(paper.title, "新题目")
        self.assertEqual(paper.requirements, "新要求")
        self.assertEqual(paper.template, "新模板")
        self.assertEqual(paper.content, "新正文")

    @patch("app.tools.ai.AIToolClass.get_ai_generate")
    def test_refactor_summary_rolls_back_on_failure(self, mock_generate):
        paper = GeneratedPaper.objects.create(
            user=self.user,
            title="旧题目",
            requirements="旧要求",
            template="旧模板",
            summary="旧总结",
        )
        mock_generate.side_effect = AIServiceError("AI service failed")

        with self.assertRaises(AIServiceError):
            aisv.refactor_summary(
                requirements="新要求",
                old_summary="旧总结",
                title="新题目",
                template_summary="新模板",
                paper_id=paper.id,
                user=self.user,
            )

        paper.refresh_from_db()
        self.assertEqual(paper.title, "旧题目")
        self.assertEqual(paper.requirements, "旧要求")
        self.assertEqual(paper.template, "旧模板")
        self.assertEqual(paper.summary, "旧总结")

    @patch("app.tools.ai.AIToolClass.get_ai_generate")
    def test_refactor_acknowledgement_updates_generated_paper(self, mock_generate):
        paper = GeneratedPaper.objects.create(
            user=self.user,
            title="旧题目",
            requirements="旧要求",
            template="旧模板",
            thank_words="旧致谢",
        )
        mock_generate.return_value = "新致谢"

        result = aisv.refactor_acknowledgement(
            requirements="新要求",
            old_acknowledgement="旧致谢",
            title="新题目",
            template_acknowledgement="新模板",
            paper_id=paper.id,
            user=self.user,
        )

        paper.refresh_from_db()
        self.assertEqual(result["thank_words"], "新致谢")
        self.assertEqual(paper.title, "新题目")
        self.assertEqual(paper.requirements, "新要求")
        self.assertEqual(paper.template, "新模板")
        self.assertEqual(paper.thank_words, "新致谢")

    @patch("app.tools.ai.AIToolClass.get_ai_generate")
    def test_refactor_reference_updates_generated_paper(self, mock_generate):
        paper = GeneratedPaper.objects.create(
            user=self.user,
            title="旧题目",
            requirements="旧要求",
            template="旧模板",
            literature=["旧参考"],
        )
        mock_generate.return_value = '["新参考1", "新参考2"]'

        result = aisv.refactor_reference(
            requirements="新要求",
            old_reference=["旧参考"],
            title="新题目",
            template_reference="新模板",
            paper_id=paper.id,
            user=self.user,
        )

        paper.refresh_from_db()
        self.assertEqual(result["literature"], ["新参考1", "新参考2"])
        self.assertEqual(paper.title, "新题目")
        self.assertEqual(paper.requirements, "新要求")
        self.assertEqual(paper.template, "新模板")
        self.assertEqual(paper.literature, ["新参考1", "新参考2"])


class GeneratePaperApiTestCase(APITestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            phone="13900000000",
            password="test-password",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @patch("app.tools.ai.AIToolClass.get_ai_translation")
    @patch("app.tools.ai.AIToolClass.get_ai_generate")
    def test_generate_paper_api_returns_paper_id(self, mock_generate, mock_translate):
        mock_generate.side_effect = [
            "中文摘要",
            "论文正文",
            "论文总结",
            "致谢内容",
            '["Ref 1", "Ref 2"]',
        ]
        mock_translate.return_value = "English Abstract"

        response = self.client.post(
            "/paper/generate/all/",
            {
                "topic": "人工智能",
                "requirements": "写一篇人工智能论文",
                "title": "人工智能论文",
                "template_abstract": "摘要模板",
                "template_body": "正文模板",
                "template_summary": "总结模板",
                "template_acknowledgement": "致谢模板",
                "template_reference": "参考文献模板",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], 200)
        self.assertIn("paper_id", response.data["data"])
        self.assertEqual(response.data["data"]["status"], "completed")
        self.assertEqual(
            GeneratedPaper.objects.get(pk=response.data["data"]["paper_id"]).content,
            "论文正文",
        )

    @patch("app.tools.ai.AIToolClass.get_ai_generate")
    def test_refactor_body_api_updates_paper(self, mock_generate):
        paper = GeneratedPaper.objects.create(
            user=self.user,
            title="旧题目",
            requirements="旧要求",
            template="旧模板",
            content="旧正文",
        )
        mock_generate.return_value = "新正文"

        response = self.client.patch(
            "/paper/generate/body/",
            {
                "paper_id": paper.id,
                "requirements": "新要求",
                "title": "新题目",
                "old_body": "旧正文",
                "template_body": "新模板",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], 200)
        self.assertEqual(response.data["data"]["content"], "新正文")
        paper.refresh_from_db()
        self.assertEqual(paper.content, "新正文")
