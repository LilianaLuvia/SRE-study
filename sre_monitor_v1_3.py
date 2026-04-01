import os
from datetime import datetime
from modules import log_utils
from modules import memory_utils
import traceback

#配置环境变量
base_dir=os.getcwd()
log_dir=os.path.join(base_dir,"logs","health.log")
FINAL=False

#检查logs文件是否存在
os.makedirs(os.path.join(base_dir,"logs"),exist_ok=True)

#方法：完整冗余内存监控
def monitor_memory(log_dir):
    MAX_SIZE=20*1024
    
    #定义返回值字典
    result={
        "success":False,
        "Status":None,
        "Available_Mem":None,
        "Usage%":None
        }
    
    try:
        print("[@] 正在进行 [Log_Rorator] ")
        
        #调用轮转函数，并接收返回值，输出轮转情况
        val_status,log_status,backup_log=log_utils.rotate_log(log_dir,MAX_SIZE)
        print(f"{val_status}\n")
        
        #备份程序完成，则进入下一步程序
        #调用内存检查函数，抓取系统当前的 available 内存数值
        if log_status is not False:
            print("[@] 正在进行 [Memory_Check] ")
            result.update(memory_utils.get_memory_info(log_dir))
            return result
        else:
            print("[@] [Log_Rorator] 程序发生未知异常 \n")
            return result
        
    except Exception:
        traceback.print_exc()
        return result

#主程序运行
if __name__=="__main__":
    monitor_memory(log_dir)    