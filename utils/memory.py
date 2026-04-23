import os
import psutil
from datetime import datetime

#方法: 数据清洗，清除"Gi"、"Mi"
def parse_to_mb(available_mem):
    if "Gi" in available_mem:
        final_men=float(available_mem.replace("Gi",""))
        return final_men*1024
    elif "Mi" in available_mem:
        final_men=float(available_mem.replace("Mi",""))
        return final_men
    else:
        return 0.0
    
#方法: 查看完整内存状态及计算压力值Usage%
def get_memory_info():  
    #抓取系统当前的 available 内存数值
    res=psutil.virtual_memory()
    total_mem=res.total
    used_mem=res.used
    usage_mem=res.percent
    
    return {
        "total_mem":f"{total_mem/(1024**3):.2f}",
        "used_mem":f"{used_mem/(1024**3):.2f}",
        "usage_mem":f"{usage_mem}"
    }
        
        

