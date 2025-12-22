from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.users'
    verbose_name = '论文管理系统' 
    label = 'app_users'

    def ready(self):
        import django.contrib.auth.signals
