import subprocess
import os
from datetime import datetime

#设定初始工作目录
base_dir=os.path.join(os.getcwd(),"logs")
full_path=os.path.join(base_dir,"health.log")

#环境检查
os.makedirs(base_dir,exist_ok=True)

#格式化当前时间
timestamp=datetime.now().strftime("%Y-%m-%d  %H:%M:%S")

#执行命令并添加状态
try:
    #使用check=True，如果命令报错会直接跳转到except
    res1=subprocess.run(['uptime','-p'],capture_output=True,text=True,check=True)
    res2=subprocess.run(['free','-h'],capture_output=True,text=True,check=True)
    
    #初始化log表格
    log=f"""
{'='*40}
检查时间：{timestamp}
系统运行时间：{res1.stdout.strip()}
内存使用情况：
{res2.stdout.strip()}
{'='*40}\n
    """
    #写入health.log文件
    with open(full_path,'a') as f:
        f.write(log)
        
except subprocess.CalledProcessError as e:
    print(f"系统命令执行失败：{e}")

#读取最新写入结果
with open(full_path,'r') as f:
    print(f.read())