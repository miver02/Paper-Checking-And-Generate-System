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
    def test_generate_abstract_creates_new_paper(self, mock_generate, mock_translate):
        old_paper = GeneratedPaper.objects.create(
            user=self.user,
            title="旧题目",
            requirements="旧要求",
            template="旧模板",
            abstract="旧摘要",
            abstract_en="Old Abstract",
        )
        mock_generate.return_value = "中文摘要"
        mock_translate.return_value = "English Abstract"

        result = aisv.generate_abstract(
            requirements="围绕人工智能生成论文摘要",
            title="人工智能研究",
            template_abstract="模板摘要",
            paper_id=old_paper.id,
            user=self.user,
        )

        self.assertEqual(GeneratedPaper.objects.count(), 2)
        old_paper.refresh_from_db()
        self.assertEqual(result["abstract_zh"], "中文摘要")
        self.assertEqual(result["abstract_en"], "English Abstract")
        self.assertEqual(old_paper.abstract, "旧摘要")
        self.assertEqual(old_paper.abstract_en, "Old Abstract")
        self.assertEqual(old_paper.title, "旧题目")
        self.assertEqual(old_paper.user_id, self.user.id)

        paper = GeneratedPaper.objects.exclude(pk=old_paper.id).get()
        self.assertEqual(paper.abstract, "中文摘要")
        self.assertEqual(paper.abstract_en, "English Abstract")
        self.assertEqual(paper.title, "人工智能研究")
        self.assertEqual(paper.user_id, self.user.id)

    @patch("app.tools.ai.AIToolClass.get_ai_translation")
    @patch("app.tools.ai.AIToolClass.get_ai_generate")
    def test_generate_paper_creates_new_paper(self, mock_generate, mock_translate):
        old_paper = GeneratedPaper.objects.create(
            user=self.user,
            title="旧题目",
            requirements="旧要求",
            template="旧模板",
            content="旧正文",
            abstract="旧摘要",
        )
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
            paper_id=old_paper.id,
            user=self.user,
        )

        self.assertEqual(GeneratedPaper.objects.count(), 2)
        old_paper.refresh_from_db()
        self.assertEqual(old_paper.title, "旧题目")
        self.assertEqual(old_paper.requirements, "旧要求")
        self.assertEqual(old_paper.template, "旧模板")
        self.assertEqual(old_paper.content, "旧正文")
        self.assertEqual(old_paper.abstract, "旧摘要")

        paper = GeneratedPaper.objects.exclude(pk=old_paper.id).get()
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
        old_paper = GeneratedPaper.objects.create(
            user=self.user,
            title="旧题目",
            requirements="旧要求",
            template="旧模板",
            content="旧正文",
        )
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
                "paper_id": old_paper.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], 200)
        self.assertIn("paper_id", response.data["data"])
        self.assertEqual(response.data["data"]["status"], "completed")
        self.assertEqual(GeneratedPaper.objects.count(), 2)
        old_paper.refresh_from_db()
        self.assertEqual(old_paper.content, "旧正文")

        new_paper = GeneratedPaper.objects.get(pk=response.data["data"]["paper_id"])
        self.assertEqual(new_paper.content, "论文正文")
        self.assertEqual(new_paper.title, "人工智能论文")
        self.assertNotEqual(new_paper.pk, old_paper.pk)
