# 模型初始化文件 
from .users import User
from .check_paper import PlagiarismCheck
from .generate_paper import GeneratedPaper
from .log import UsedLog

# 导出模型
__all__ = [
    'User',
    'GeneratedPaper',
    'PlagiarismCheck',
    'UsedLog',
]

# 引用外部文件