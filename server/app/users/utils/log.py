# utils/log.py 示例
import logging
import os
from django.conf import settings

def init_logger():
    logger = logging.getLogger("pgcs")
    logger.setLevel(logging.INFO)
    
    # 日志文件路径
    log_path = os.path.join(settings.BASE_DIR, "logs")
    os.makedirs(log_path, exist_ok=True)
    
    # 配置文件处理器
    handler = logging.FileHandler(os.path.join(log_path, "app.log"))
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger

# 导出全局logger实例
logger = init_logger()