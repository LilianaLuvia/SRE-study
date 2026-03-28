import os
import subprocess
from datetime import datetime

#设置初始工作路径

base_path=os.path.join(os.getcwd(),"logs")
log_path=os.path.join(base_path,"health.log")

#查看内存冗余及内存状态
def get_memory_info():
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
        return status,available_mem
        
    except subprocess.CalledProcessError as e:
        print(f"命令运行出错：{e}")
        return None,None

#写入日志及检查日志文件大小
def write_to_log(report_content):
    try:
        #环境检查
        os.makedirs(base_path,exist_ok=True)
        
        #在兼顾性能与安全的情况下,将当前冗余内存及状态写入日志文件
        with open(log_path,'a') as f:
            f.write(report_content)

        #额外检查文件状态
        file_size=os.path.getsize(log_path)
        
        return True,file_size
        
    except Exception as e:
        print(f"写入日志失败：{e}")
        return None,0

#主程序运行
if __name__=="__main__":

    # 1.格式化当前时间，确保时间与每次运行时间对应
    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 2.获取内存信息
    status,available_mem=get_memory_info()
    
    if status and available_mem:
        report=f"""
{"="*40}
{now} [Memory_Check] Status: {status} | Available: {available_mem}
{"="*40}\n
        """
        
        # 3.尝试写入日志文件
        success_status,file_size=write_to_log(report)
        
        # 4.检查是否写入成功
        if success_status:
            print(f"{report}")
            print(f"监控完成，当前日志大小为：{file_size} 字节")
    else:
        print("无法生成日志")
