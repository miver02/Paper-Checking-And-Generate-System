# utils/common.py 示例
from datetime import datetime


# 时间戳转格式化字符串
def timestamp_to_str(timestamp, fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.fromtimestamp(timestamp).strftime(fmt)


# 空值处理（将None/空字符串转为指定默认值）
def empty_default(value, default=""):
    return value if value is not None and value != "" else default
