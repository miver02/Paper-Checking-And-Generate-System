from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import PaperTopic, GeneratedPaper, PlagiarismCheck, UserProfile
from .serializers import (
    PaperTopicSerializer, GeneratedPaperSerializer, PlagiarismCheckSerializer,
    UserProfileSerializer, CreatePaperSerializer, CreatePlagiarismCheckSerializer
)
from .tasks import generate_paper_task, check_plagiarism_task

# Web页面视图
def home(request):
    """首页"""
    return render(request, 'papers/home.html')


@login_required
def dashboard(request):
    """用户仪表板"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    recent_papers = GeneratedPaper.objects.filter(user=request.user).order_by('-created_at')[:5]
    recent_checks = PlagiarismCheck.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'profile': profile,
        'recent_papers': recent_papers,
        'recent_checks': recent_checks,
    }
    return render(request, 'papers/dashboard.html', context)


@login_required
def generate_paper_page(request):
    """论文生成页面"""
    topics = PaperTopic.objects.all()
    return render(request, 'papers/generate_paper.html', {'topics': topics})


@login_required
def check_plagiarism_page(request):
    """查重检测页面"""
    papers = GeneratedPaper.objects.filter(user=request.user, status='completed')
    return render(request, 'papers/check_plagiarism.html', {'papers': papers})


@login_required
def paper_detail(request, paper_id):
    """论文详情页面"""
    paper = get_object_or_404(GeneratedPaper, id=paper_id, user=request.user)
    return render(request, 'papers/paper_detail.html', {'paper': paper})


@login_required
def plagiarism_detail(request, check_id):
    """查重详情页面"""
    check = get_object_or_404(PlagiarismCheck, id=check_id, user=request.user)
    return render(request, 'papers/plagiarism_detail.html', {'check': check})


def register(request):
    """用户注册"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'账户 {username} 创建成功！')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# API视图集
class PaperTopicViewSet(viewsets.ReadOnlyModelViewSet):
    """论文主题API视图集"""
    queryset = PaperTopic.objects.all()
    serializer_class = PaperTopicSerializer
    permission_classes = [IsAuthenticated]


class GeneratedPaperViewSet(viewsets.ModelViewSet):
    """生成论文API视图集"""
    serializer_class = GeneratedPaperSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return GeneratedPaper.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def create_and_generate(self, request):
        """创建并开始生成论文"""
        serializer = CreatePaperSerializer(data=request.data)
        if serializer.is_valid():
            # 创建论文记录
            paper_data = serializer.validated_data
            paper = GeneratedPaper.objects.create(
                user=request.user,
                title=paper_data['title'],
                topic_id=paper_data.get('topic_id'),
                requirements=paper_data['requirements'],
                model_used=paper_data.get('model_used', 'gpt-3.5-turbo'),
                temperature=paper_data.get('temperature', 0.7),
                max_tokens=paper_data.get('max_tokens', 4000),
                status='generating'
            )
            
            # 启动异步生成任务
            generate_paper_task.delay(paper.id)
            
            return Response({
                'id': paper.id,
                'message': '论文生成任务已启动',
                'status': 'generating'
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """获取论文生成状态"""
        paper = self.get_object()
        return Response({
            'id': paper.id,
            'status': paper.status,
            'word_count': paper.word_count,
            'completed_at': paper.completed_at
        })


class PlagiarismCheckViewSet(viewsets.ModelViewSet):
    """查重检测API视图集"""
    serializer_class = PlagiarismCheckSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PlagiarismCheck.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def create_and_check(self, request):
        """创建并开始查重检测"""
        serializer = CreatePlagiarismCheckSerializer(data=request.data)
        if serializer.is_valid():
            # 创建查重记录
            check_data = serializer.validated_data
            check = PlagiarismCheck.objects.create(
                user=request.user,
                title=check_data['title'],
                content=check_data['content'],
                paper_id=check_data.get('paper_id'),
                status='processing'
            )
            
            # 启动异步查重任务
            check_plagiarism_task.delay(check.id)
            
            return Response({
                'id': check.id,
                'message': '查重检测任务已启动',
                'status': 'processing'
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """获取查重检测状态"""
        check = self.get_object()
        return Response({
            'id': check.id,
            'status': check.status,
            'similarity_percentage': check.similarity_percentage,
            'completed_at': check.completed_at
        })


class UserProfileViewSet(viewsets.ModelViewSet):
    """用户配置API视图集"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """获取当前用户配置"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


# API函数视图
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stats(request):
    """获取用户统计信息"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    recent_papers = GeneratedPaper.objects.filter(user=request.user).order_by('-created_at')[:5]
    recent_checks = PlagiarismCheck.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    return Response({
        'papers_generated': profile.papers_generated,
        'plagiarism_checks': profile.plagiarism_checks,
        'recent_papers': GeneratedPaperSerializer(recent_papers, many=True).data,
        'recent_checks': PlagiarismCheckSerializer(recent_checks, many=True).data
    }) 


@api_view(['POST'])
@permission_classes([AllowAny])
def vue_login(request):
    """Vue前端登录API"""
    username = request.data.get('username')
    password = request.data.get('password')

    if username and password:
        user = IsAuthenticated(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            })
        else:
            return Response({'error': '用户名或密码错误'}, status=400)
    else:
        return Response({'error': '请提供用户名和密码'}, status=400)