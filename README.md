# 论文生成和查重系统

基于 Django 框架开发的论文生成和查重系统，集成了 AI 模型生成功能和第三方查重 API。

## 功能特色

### 🤖 论文生成模块

- 使用 OpenAI GPT 模型生成学术论文
- 支持自定义论文主题和要求
- 可调节生成参数（温度、最大令牌数等）
- 异步处理，提高用户体验

### 🔍 查重检测模块

- 集成第三方查重 API
- 支持相似度检测和详细报告
- 模拟查重功能（用于演示）
- 查重历史记录管理

### 👤 用户管理

- 用户注册、登录、认证
- 个人仪表板
- 使用统计和历史记录
- 用户偏好设置

### 🎨 现代化界面

- 响应式设计，支持移动端
- Bootstrap 5 + Font Awesome
- 直观的用户界面
- 实时状态更新

## 技术栈

- **后端**: Django 4.2 + Django REST Framework
- **数据库**: SQLite (可扩展为 PostgreSQL/MySQL)
- **异步任务**: Celery + Redis
- **AI 模型**: OpenAI GPT
- **前端**: Bootstrap 5 + jQuery
- **部署**: 支持 Docker 部署

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd Paper-Checking-And-Generate-System

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 环境配置

```bash
# 复制环境变量文件
cp .env.example .env

# 编辑 .env 文件，配置以下参数：
# - SECRET_KEY: Django密钥
# - OPENAI_API_KEY: OpenAI API密钥
# - PLAGIARISM_API_KEY: 查重API密钥（可选）
# - REDIS_URL: Redis连接URL
```

### 3. 数据库初始化

```bash
# 创建迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 创建论文主题数据（可选）
python manage.py shell
>>> from papers.models import PaperTopic
>>> PaperTopic.objects.create(name="计算机科学", description="计算机科学相关论文")
>>> PaperTopic.objects.create(name="人工智能", description="AI和机器学习相关论文")
>>> exit()
```

### 4. 启动服务

```bash
# 启动Redis服务器（另开终端）
redis-server

# 启动Celery工作进程（另开终端）
celery -A celery_app worker --loglevel=info

# 启动Django开发服务器
python manage.py runserver
```

### 5. 访问系统

- 主页: http://127.0.0.1:8000/
- 管理后台: http://127.0.0.1:8000/admin/
- API 文档: http://127.0.0.1:8000/api/

## API 接口

### 论文生成 API

```bash
# 创建并生成论文
POST /api/papers/create_and_generate/
{
    "title": "论文标题",
    "topic_id": 1,
    "requirements": "论文要求",
    "model_used": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 4000
}

# 查询生成状态
GET /api/papers/{id}/status/
```

### 查重检测 API

```bash
# 创建并开始查重
POST /api/plagiarism/create_and_check/
{
    "title": "检测标题",
    "content": "论文内容",
    "paper_id": 1
}

# 查询检测状态
GET /api/plagiarism/{id}/status/
```

## 项目结构

```
Paper-Checking-And-Generate-System/
├── paper/           # Django项目配置
│   ├── settings.py        # 项目设置
│   ├── urls.py           # 主URL配置
│   └── ...
├── papers/                # 主应用
│   ├── models.py         # 数据模型
│   ├── views.py          # 视图函数
│   ├── serializers.py    # API序列化器
│   ├── services.py       # 业务逻辑
│   ├── tasks.py          # Celery任务
│   └── ...
├── templates/             # HTML模板
│   ├── base.html         # 基础模板
│   ├── papers/           # 应用模板
│   └── registration/     # 认证模板
├── static/               # 静态文件
├── media/                # 媒体文件
├── requirements.txt      # Python依赖
├── .env.example         # 环境变量示例
└── README.md            # 项目说明
```

## 部署说明

### Docker 部署

```bash
# 构建镜像
docker build -t paper-system .

# 运行容器
docker run -d -p 8000:8000 --env-file .env paper-system
```

### 生产环境配置

1. 使用 PostgreSQL 或 MySQL 数据库
2. 配置 Nginx 反向代理
3. 使用 Gunicorn 作为 WSGI 服务器
4. 配置 SSL 证书
5. 设置定时任务和监控

## 注意事项

1. **API 密钥安全**: 请妥善保管 OpenAI API 密钥，避免泄露
2. **查重 API**: 默认使用模拟查重，生产环境需配置真实 API
3. **Redis 服务**: Celery 需要 Redis 服务支持异步任务
4. **资源限制**: 注意 AI 生成的 token 消耗和 API 调用频率限制

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交代码
4. 发起 Pull Request

## 许可证

MIT License

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件

---

**注意**: 本系统仅用于学术研究和教育目的，请遵守相关法律法规和学术道德规范。
