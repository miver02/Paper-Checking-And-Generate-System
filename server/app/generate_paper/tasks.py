# from celery import shared_task


# @shared_task
# def generate_paper_task(paper_id):
#     """异步生成论文任务"""
#     from .services import PaperGenerationService
#     service = PaperGenerationService()
#     return service.generate_paper(paper_id)


# @shared_task
# def check_plagiarism_task(check_id):
#     """异步查重检测任务"""
#     from .services import PlagiarismCheckService
#     service = PlagiarismCheckService()
#     return service.check_plagiarism(check_id) 