from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.users'
    verbose_name = '用户模块' 
    label = 'app_users'

