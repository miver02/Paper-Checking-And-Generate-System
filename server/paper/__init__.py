# 这使得paper成为一个Python包 
import os
import pymysql
from django.conf import settings

pymysql.install_as_MySQLdb()

# 连接Mysql并创建数据库（仅首次执行）
def create_database():
    conn = pymysql.connect(
        host = settings.DATABASES['default']['HOST'],
        user = settings.DATABASES['default']['USER'],
        password = settings.DATABASES['default']['PASSWORD'],
        port = settings.DATABASES['default']['PORT'],
        charset = 'utf8mb4',
        autocommit = True,
    )
    cursor = conn.cursor()
    # 创建数据库
    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {settings.DATABASES["default"]["NAME"]} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;')
    cursor.close()



def create_media_directory():
    try:
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            print(f"Media directory created: {settings.MEDIA_ROOT}")
    except Exception as e:
        print(f"Failed to create media directory: {e}")


if settings.DATABASES["default"]["ENGINE"] == "django.db.backends.mysql":
    create_database()
create_media_directory()
