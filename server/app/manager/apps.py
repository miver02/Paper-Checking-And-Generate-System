from django.apps import AppConfig


class ManagersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.manager'
    verbose_name = '论文管理系统' 
    label = 'app_manager'