import os
import subprocess
from datetime import datetime

#设置初始工作路径

base_path=os.path.join(os.getcwd(),"logs")
log_path=os.path.join(base_path,"health.log")

#环境检查
os.makedirs(base_path,exist_ok=True)

#格式化当前时间
now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#执行命令
try:
    res=subprocess.run(['free','-h'],capture_output=True,text=True,check=True)

    #裁切"free -h"运行的结果
    lines=res.stdout.splitlines()
    parts=lines[1].split()

    #提取可用内存
    available_mem=parts[6]

    #逻辑判断内存
    if "Gi" in available_mem:
        is_low=False
    elif "Mi" in available_mem:
        mem=int(available_mem.replace("Mi",""))
        is_low=mem<100
    else:
        is_low=True

    status="内存告急" if is_low else "内存充足"

    report=f"""
{"="*40}
{now} [Memory_Check] Status: {status} | Available: {available_mem}
{"="*40}\n
    """

    #在兼顾性能与安全的情况下,将当前冗余内存及状态写入日志文件
    with open(log_path,'a') as f:
        f.write(report)
        
    #核验程序运行成功
    print("本次内存监控报告已成功写入：")
    print(report.strip())

    #额外检查文件状态

    file_size=os.path.getsize(log_path)
    print(f"当前日志总大小：{file_size} 字节")

except subprocess.CalledProcessError as e:
    print(f"系统运行命令失败：{e}")
except Exception as e:
    print(f"写入失败！发生未知错误：{e}")