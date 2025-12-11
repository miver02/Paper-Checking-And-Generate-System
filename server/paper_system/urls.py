"""
URL configuration for paper_system project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.papers.urls')),
    path('', include('app.papers.urls')),  # 主页面路由

    # Vue前端路由（必须放在最后）
    # re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]

# 开发环境下提供静态文件和媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 