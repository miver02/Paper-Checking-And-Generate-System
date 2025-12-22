"""
Django settings for paper project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv('./.env')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    # 'app.manager', 
    'app.users',  
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # 处理跨域资源共享
    'django.middleware.security.SecurityMiddleware', # 提供各种安全保护
    'django.contrib.sessions.middleware.SessionMiddleware', # 管理会话
    'django.middleware.common.CommonMiddleware', # 提供常用的http处理功能
    'django.middleware.csrf.CsrfViewMiddleware', # 防止跨站请求伪造攻击
    'django.contrib.auth.middleware.AuthenticationMiddleware', # 处理用户认证
    'django.contrib.messages.middleware.MessageMiddleware', # 处理一次性消息
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # 防止点击劫持攻击
]

ROOT_URLCONF = 'paper.urls'
 
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'paper.wsgi.application'

# Database
if os.getenv('DB_ENGINE') == 'mysql':
    # mysql 配置
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME', 'pgcs'),
            'USER': os.getenv('DB_USER', 'pgcs'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'pgcs'),
            'HOST': os.getenv('DB_HOST', '0.0.0.0'),
            'PORT': int(os.getenv('DB_PORT', '0000')),
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES';",
                'use_unicode': True,
                'charset': 'utf8mb4',
                'autocommit': True,
            },
            'CONN_MAX_AGE': 60,
        }
    }
    # Redis 配置（缓存/会话）
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': os.getenv('REDIS_URL', 'pgcs'),  # Docker Redis 地址+数据库编号
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'PASSWORD': os.getenv('REDIS_PASSWORD', 'pgcs'),
            }
        }
    }
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'default'
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3'
        }
    }
    # SQLite模式下使用本地内存缓存
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR / 'static']
# STATIC_ROOT = BASE_DIR / 'staticfiles'

# 添加Vue构建文件的路径
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR / 'static/web/dist',  # 如果Vue项目在web目录下
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [ 
        'rest_framework.permissions.IsAuthenticated', # 设置访问权限:未登录用户无法访问
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [ 
        'rest_framework.authentication.TokenAuthentication',  # 使用token认证
        'rest_framework.authentication.SessionAuthentication', # 保留session认证
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination', # 自动为api响应分页
    'PAGE_SIZE': 20, # 每页显示20条数据
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# AI模型设置
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')

# 查重API设置
PLAGIARISM_API_KEY = os.getenv('PLAGIARISM_API_KEY')
PLAGIARISM_API_URL = os.getenv('PLAGIARISM_API_URL')

# Celery设置
CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE 

# 指定自定义用户模型（关键！）
AUTH_USER_MODEL = "app_users.User"