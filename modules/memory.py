import os
import subprocess
from datetime import datetime

#设置初始工作路径

base_dir=os.path.join(os.getcwd(),"logs")
log_dir=os.path.join(base_dir,"health.log")

#方法：数据清洗，清除"Gi"、"Mi"
def parse_to_mb(available_mem):
    if "Gi" in available_mem:
        return float(available_mem.replace("Gi","")),"Gi"
    elif "Mi" in available_mem:
        return float(available_mem.replace("Mi","")),"Mi"
    else:
        return 0.0,None
    
#方法：数据折算单位"Mi"
def convert_to_mb(value,unit):
    if unit=="Gi":
        return value*1024
    elif unit=="Mi":
        return value
    else:
        return 0.0
    
#方法：查看内存冗余、内存状态及计算压力值Usage%,并写入日志
def get_memory_info(log_dir):
    
    #定义返回值字典
    result={
        "success":False,
        "Status":None,
        "Available_Mem":None,
        "Usage%":None
        }
        
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

        #提取总内存及冗余内存,数据清洗，去除单位
        total_mem_str,total_unit=parse_to_mb(parts[1])
        available_mem_str,available_unit=parse_to_mb(parts[6])
        
        #将内存值折算成Mi
        total_mem=convert_to_mb(total_mem_str,total_unit)
        available_mem=convert_to_mb(available_mem_str,available_unit)
         
        #逻辑判断内存
        if available_mem<100:
            is_low=True
        else:
            is_low=False
        
        status="内存告急" if is_low else "内存充足"
        
        #计算压力值Usage%
        usage_percent=(total_mem-available_mem)/total_mem*100
        
        #在兼顾性能与安全的情况下,将当前冗余内存及状态写入日志文件
        report=f"""
{"="*50}\n
{now} [Memory_Check] 
Status: {status} | Available: {available_mem} Mi | Usage%: {usage_percent:.2f}%\n
{"="*50}
                    """
        with open(log_dir,'a') as f:
            f.write(report)
        print(report)
        
        #将数据计入字典，程序运行返回数据以字典形式作返回值,以便后续分析使用
        result.update({
                "success":True,
                "Status":f"{status}",
                "Available_Mem":available_mem,
                "Usage%":f"{usage_percent:.2f}%"
            })
            
        return result
        
    except subprocess.CalledProcessError as e:
        print(f"命令运行出错：{e}")
        return result

#主程序运行
if __name__=="__main__":

    # 1.格式化当前时间，确保时间与每次运行时间对应
    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 2.获取内存信息
    res=get_memory_info(log_dir)

