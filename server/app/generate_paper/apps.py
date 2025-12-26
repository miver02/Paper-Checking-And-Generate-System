from django.apps import AppConfig


class GeneratePaperConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.generate_paper"
    label = "app_generate_paper"
    verbose_name = "论文生成模块"