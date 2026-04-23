import os
from datetime import datetime
from utils import log
from utils import memory
import traceback

#配置环境变量
base_dir=os.getcwd()
log_path=os.path.join(base_dir,"logs","health.log")
FINAL=False

#检查logs文件是否存在
os.makedirs(os.path.join(base_dir,"logs"),exist_ok=True)

#方法: 完整冗余内存监控
def monitor_memory(log_path):
    mAX_SIZE=20*1024
    
    #定义返回值字典
    result={
        "success":False,
        "status":None,
        "available_mem":None,
        "usage":None
        }
    
    try:
        print("[@] 正在进行 [Log_Rorator] ")
        
        #调用轮转函数，并接收返回值，输出轮转情况
        rotate_res=log.rotate_log(log_path,mAX_SIZE)
        rotate_success=rotate_res.get("success")
        print(f"{rotate_success}\n")
        
        #备份程序完成，则进入下一步程序
        #调用内存检查函数，抓取系统当前的 available 内存数值
        if rotate_success:
            mem_check_res=memory.get_memory_info()
            result.update({
                "success":rotate_success,
                "status":rotate_res.get("status"),
                "available_mem":mem_check_res.get("available_mem"),
                "usage":mem_check_res.get("usage")
            })
            return result
        else:
            return result
        
    except Exception:
        traceback.print_exc()
        return result

#主程序运行
if __name__=="__main__":
    result=monitor_memory(log_path)    
    print(result)