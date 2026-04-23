from datetime import datetime

#方法: 获取格式化标准时间
def now():
    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return now