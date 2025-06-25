from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views

# API路由
router = DefaultRouter()
router.register(r'topics', views.PaperTopicViewSet)
router.register(r'papers', views.GeneratedPaperViewSet, basename='papers')
router.register(r'plagiarism', views.PlagiarismCheckViewSet, basename='plagiarism')
router.register(r'profile', views.UserProfileViewSet, basename='profile')

urlpatterns = [
    # Web页面路由
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('generate/', views.generate_paper_page, name='generate_paper'),
    path('check/', views.check_plagiarism_page, name='check_plagiarism'),
    path('paper/<int:paper_id>/', views.paper_detail, name='paper_detail'),
    path('plagiarism/<int:check_id>/', views.plagiarism_detail, name='plagiarism_detail'),
    
    # 用户认证路由
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # API路由
    path('api/', include(router.urls)),
    path('api/stats/', views.user_stats, name='user_stats'),
] 