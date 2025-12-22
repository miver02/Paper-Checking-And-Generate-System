# PGCS 论文生成与查重系统 - 项目架构说明

## 项目概述

本项目是一个基于Django的论文生成与查重检测系统，主要包含两个应用：`users` 和 `manager`。系统支持论文自动生成、查重检测等功能，采用前后端分离架构，提供Web界面和RESTful API接口。

## 项目结构
```
server/
├── app/
│   ├── manager/              # 管理员应用
│   │   ├── __init__.py       # 应用初始化文件
│   │   ├── admin.py          # 后台管理配置（待完善）
│   │   ├── apps.py           # 应用配置
│   │   ├── models.py         # 数据模型（待完善）
│   │   ├── serializers.py    # 序列化器（待完善）
│   │   ├── services.py       # 业务逻辑服务（待完善）
│   │   ├── tasks.py          # 异步任务（待完善）
│   │   ├── urls.py           # URL路由配置
│   │   └── views.py          # 视图控制器（待完善）
│   └── users/                # 用户应用
│       ├── __init__.py       # 应用初始化文件
│       ├── admin.py          # 后台管理配置
│       ├── apps.py           # 应用配置
│       ├── models/           # 数据模型目录
│       │   ├── __init__.py   # 模型初始化文件
│       │   ├── check_paper.py# 查重检测模型
│       │   ├── generate_paper.py # 论文生成模型
│       │   ├── log.py        # 使用日志模型
│       │   └── users.py      # 用户模型
│       ├── serializers.py    # 序列化器
│       ├── services.py       # 业务逻辑服务
│       ├── tasks.py          # 异步任务
│       ├── urls.py           # URL路由配置
│       ├── utils/            # 工具类目录
│       │   ├── __init__.py   # 工具初始化文件
│       │   ├── common.py     # 通用工具函数
│       │   └── log.py        # 日志工具
│       └── views.py          # 视图控制器
```

## 文件详细说明

### manager 应用（论文管理系统）

#### `__init__.py`
- 应用初始化文件，标识该目录为Python包

#### [apps.py](file:///home/miver/githome/pgcs/server/app/users/apps.py)
- 应用配置文件，定义应用的基本信息和元数据
- 配置项包括应用名称、显示名称等

#### [admin.py](file:///home/miver/githome/pgcs/server/app/users/admin.py)
- Django后台管理界面配置文件（目前为空，待完善）
- 将用于注册模型到Django Admin后台进行管理

#### [models.py](file:///home/miver/githome/pgcs/server/app/manager/models.py)
- 数据模型定义文件（目前为空，待完善）
- 预计将包含系统管理相关的数据模型

#### [views.py](file:///home/miver/githome/pgcs/server/app/users/views.py)
- 视图控制器文件（目前为空，待完善）
- 将包含管理端相关的视图处理逻辑

#### [urls.py](file:///home/miver/githome/pgcs/server/paper/urls.py)
- URL路由配置文件
- 目前包含示例路由配置，需要根据实际管理功能进行完善

#### [serializers.py](file:///home/miver/githome/pgcs/server/app/users/serializers.py)
- REST API序列化器文件（目前为空，待完善）
- 用于将模型实例序列化为JSON格式数据

#### `services.py`
- 业务逻辑服务文件（目前为空，待完善）
- 包含管理端的核心业务逻辑实现

#### [tasks.py](file:///home/miver/githome/pgcs/server/app/users/tasks.py)
- 异步任务定义文件（目前为空，待完善）
- 使用Celery定义后台异步任务

### users 应用（用户相关功能）

#### [__init__.py](file:///home/miver/githome/pgcs/server/core/__init__.py)
- 应用初始化文件，标识该目录为Python包

#### [apps.py](file:///home/miver/githome/pgcs/server/app/users/apps.py)
- 应用配置文件，定义应用的基本信息和元数据
- 配置了应用名称和显示名称为"论文管理系统"

#### `admin.py`
- Django后台管理界面配置文件
- 注册了以下模型到Admin后台：
  - PaperTopic（论文主题）
  - GeneratedPaper（生成的论文）
  - PlagiarismCheck（查重检测）
  - UserProfile（用户资料）

#### `models/` 目录

##### [__init__.py](file:///home/miver/githome/pgcs/server/core/__init__.py)
- 模型初始化文件
- 导出核心模型：User、GeneratedPaper、PlagiarismCheck

##### [users.py](file:///home/miver/githome/pgcs/server/app/users/models/users.py)
- 用户模型定义文件
- 实现了自定义用户模型（继承AbstractBaseUser）
- 支持手机号登录，包含用户名、手机号、邮箱、头像等字段
- 提供用户管理器CustomUserManager用于创建用户

##### [generate_paper.py](file:///home/miver/githome/pgcs/server/app/users/models/generate_paper.py)
- 论文生成模型定义文件
- 包含GeneratedPaper（生成论文记录）模型
- 记录论文生成请求、要求、模板、生成内容及相关状态信息
- 包含生成状态跟踪和时间记录

##### [check_paper.py](file:///home/miver/githome/pgcs/server/app/users/models/check_paper.py)
- 查重检测模型定义文件
- 包含PlagiarismCheck（查重检测记录）模型
- 记录查重检测请求、内容、结果及相关状态信息
- 包含相似度百分比、报告链接等字段

##### [log.py](file:///home/miver/githome/pgcs/server/app/users/models/log.py)
- 使用日志模型定义文件
- 包含UsedLog（使用日志）模型
- 记录用户使用模型的行为日志，包括操作类型、模型名称、token消耗等

#### [views.py](file:///home/miver/githome/pgcs/server/app/users/views.py)
- 视图控制器文件
- 包含Web页面视图和REST API视图
- Web页面包括：首页、仪表板、论文生成页、查重检测页等
- API视图集包括：论文主题、生成论文、查重检测、用户配置等
- 提供用户注册和登录功能

#### [urls.py](file:///home/miver/githome/pgcs/server/app/users/urls.py)
- URL路由配置文件
- 配置Web页面路由和API路由
- 使用DRF路由器自动注册API视图集
- 包含用户认证相关路由

#### [serializers.py](file:///home/miver/githome/pgcs/server/app/users/serializers.py)
- REST API序列化器文件
- 定义了各个模型的序列化器
- 包括用户、论文主题、生成论文、查重检测、用户配置等序列化器
- 提供创建论文和查重检测的简化序列化器

#### [services.py](file:///home/miver/githome/pgcs/server/app/users/services.py)
- 业务逻辑服务文件
- 包含PaperGenerationService（论文生成服务）和PlagiarismCheckService（查重检测服务）
- 实现与外部API交互的逻辑（如OpenAI）
- 处理论文生成和查重检测的核心业务逻辑

#### [tasks.py](file:///home/miver/githome/pgcs/server/app/users/tasks.py)
- 异步任务定义文件
- 使用Celery定义异步任务
- 包含generate_paper_task（论文生成任务）和check_plagiarism_task（查重检测任务）

#### `utils/` 目录

##### [__init__.py](file:///home/miver/githome/pgcs/server/core/__init__.py)
- 工具初始化文件
- 导入并导出通用工具

##### `common.py`
- 通用工具函数文件
- 包含时间戳转换和空值处理等常用函数

##### `log.py`
- 日志工具文件
- 初始化并配置应用日志记录器

## 核心功能流程

1. **用户注册与登录**
   - 用户通过手机号注册和登录系统
   - 提供Web界面和API两种方式

2. **论文生成**
   - 用户填写论文要求和主题
   - 系统调用AI模型生成论文内容
   - 异步任务处理生成过程
   - 生成完成后更新状态和统计数据

3. **查重检测**
   - 用户提交论文内容进行查重
   - 系统调用查重服务进行检测
   - 返回相似度百分比和检测报告
   - 记录检测结果和统计数据

4. **数据管理**
   - 通过Django Admin后台管理各类数据
   - 提供用户、论文、查重记录的查看和编辑功能
   - 支持数据统计和分析

## 技术特点

1. **前后端分离架构**
   - 提供RESTful API供前端调用
   - 支持Web界面和Vue前端

2. **异步任务处理**
   - 使用Celery处理耗时任务
   - 提高系统响应速度和用户体验

3. **灵活的数据模型**
   - 自定义用户模型支持手机号登录
   - 完整的论文生成和查重数据记录

4. **完善的后台管理**
   - 通过Django Admin提供可视化数据管理
   - 支持搜索、过滤和批量操作

