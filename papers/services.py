import openai
import requests
import json
import logging
from typing import Dict, Any, Optional
from django.conf import settings
from django.utils import timezone
from .models import GeneratedPaper, PlagiarismCheck, UserProfile

logger = logging.getLogger(__name__)


class PaperGenerationService:
    """论文生成服务"""
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        if self.api_key:
            openai.api_key = self.api_key
    
    def generate_paper(self, paper_id: int) -> Dict[str, Any]:
        """生成论文内容"""
        try:
            paper = GeneratedPaper.objects.get(id=paper_id)
            paper.status = 'generating'
            paper.save()
            
            # 构建提示词
            prompt = self._build_prompt(paper)
            
            # 调用OpenAI API
            response = openai.ChatCompletion.create(
                model=paper.model_used,
                messages=[
                    {"role": "system", "content": "你是一个专业的学术论文写作助手。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=paper.max_tokens,
                temperature=paper.temperature,
                stream=False
            )
            
            # 提取生成的内容
            generated_content = response.choices[0].message.content
            
            # 更新论文内容
            paper.content = generated_content
            paper.status = 'completed'
            paper.completed_at = timezone.now()
            paper.save()
            
            # 更新用户统计
            profile, created = UserProfile.objects.get_or_create(user=paper.user)
            profile.papers_generated += 1
            profile.save()
            
            return {
                'success': True,
                'content': generated_content,
                'word_count': paper.word_count,
                'message': '论文生成成功'
            }
            
        except Exception as e:
            logger.error(f"论文生成失败: {str(e)}")
            return {'success': False, 'message': f'生成失败: {str(e)}'}
    
    def _build_prompt(self, paper: GeneratedPaper) -> str:
        """构建生成提示词"""
        topic_info = f"主题: {paper.topic.name}" if paper.topic else ""
        
        prompt = f"""请根据以下要求生成一篇学术论文：

{topic_info}
论文标题: {paper.title}

具体要求:
{paper.requirements}

请生成一篇结构完整的学术论文。"""
        
        return prompt


class PlagiarismCheckService:
    """查重检测服务"""
    
    def check_plagiarism(self, check_id: int) -> Dict[str, Any]:
        """执行查重检测"""
        try:
            check = PlagiarismCheck.objects.get(id=check_id)
            check.status = 'processing'
            check.save()
            
            # 模拟查重结果
            import random
            similarity = round(random.uniform(5.0, 25.0), 2)
            
            check.similarity_percentage = similarity
            check.status = 'completed'
            check.completed_at = timezone.now()
            check.save()
            
            return {
                'success': True,
                'similarity_percentage': similarity,
                'message': '查重检测完成'
            }
            
        except Exception as e:
            logger.error(f"查重检测失败: {str(e)}")
            return {'success': False, 'message': f'检测失败: {str(e)}'} 