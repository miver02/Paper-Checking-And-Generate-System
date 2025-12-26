from django.apps import AppConfig


class PlagiarismCheckConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.plagiarism_check"
    label = "app_plagiarism_check"
    verbose_name = "论文查重模块"