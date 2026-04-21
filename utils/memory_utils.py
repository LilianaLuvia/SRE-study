import os
import subprocess
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
    MAX_SIZE=20*1024
    
    #定义返回值字典
    result={
        "Success":False,
        "Status":None,
        "Available_Mem":None,
        "Usage":None
        }
        
    try:
        
        #抓取系统当前的 available 内存数值
        res=subprocess.run(['free','-h'],capture_output=True,text=True,check=True)

        #裁切"free -h"运行的结果
        lines=res.stdout.splitlines()
        parts=lines[1].split()

        #提取总内存及冗余内存,数据清洗，去除单位
        total_mem=parse_to_mb(parts[1])
        available_mem=parse_to_mb(parts[6])

        #逻辑判断内存
        if available_mem<100:
            is_low=True
        else:
            is_low=False
        
        status="内存告急" if is_low else "内存充足"
        
        #计算压力值Usage%
        usage_percent=(total_mem-available_mem)/total_mem*100
        
        #将数据计入字典，程序运行返回数据以字典形式作返回值,以便后续分析使用
        result.update({
                "Success":True,
                "Status":status,
                "Available_Mem":available_mem,
                "Usage":f"{usage_percent:.2f}"
            })
            
        return result
        
    except subprocess.CalledProcessError as e:
        print(f"命令运行出错: {e}")
        return result

