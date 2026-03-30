import os
import subprocess
from datetime import datetime

#设置初始工作路径

base_dir=os.path.join(os.getcwd(),"logs")
log_dir=os.path.join(base_dir,"health.log")

#方法：查看内存冗余及内存状态,并写入日志
def get_memory_info(log_dir):
    try:
        
        now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_parent_dir=os.path.dirname(log_dir)
        os.makedirs(log_parent_dir,exist_ok=True)
    
        if not os.path.exists(log_dir) :
            with open(log_dir,"w") as f :
                f.write(f"health.log has been created just now   --- {now}\n\n")
        
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
        
        #在兼顾性能与安全的情况下,将当前冗余内存及状态写入日志文件
        report=f"""
{"="*50}\n
{now} [Memory_Check] Status: {status} | Available: {available_mem}\n
{"="*50}
                    """
        with open(log_dir,'a') as f:
            f.write(report)
        print(report)
            
        return True,status,available_mem
        
    except subprocess.CalledProcessError as e:
        print(f"命令运行出错：{e}")
        return False,None,None

#主程序运行
if __name__=="__main__":

    # 1.格式化当前时间，确保时间与每次运行时间对应
    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 2.获取内存信息
    final,status,available_mem=get_memory_info(log_dir)

