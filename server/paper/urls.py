"""
URL configuration for paper project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # 管理后台
    path('user/', include('app.users.urls')),  # 主页面路由
    path('security/', include('app.security.urls')),  # 安全模块
    path('paper/generate/', include('app.generate_paper.urls')), # 论文生成模块
    # path('paper/check/', include('app.plagiarism_check.urls')), # 查重模块

    # Vue前端路由（必须放在最后）
    # re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]

# 开发环境下提供静态文件和媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
