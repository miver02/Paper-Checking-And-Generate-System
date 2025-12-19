from django.apps import AppConfig


class PapersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.users'
    verbose_name = '论文管理系统' 

    def ready(self):
        import django.contrib.auth.signals

