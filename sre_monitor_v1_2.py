import os
import subprocess
from datetime import datetime
from modules import logger
from modules import memory

#配置环境变量
base_dir=os.getcwd()
log_dir=os.path.join(base_dir,"logs","health.log")
MAX_SIZE=6*1024
FINAL=False

#检查logs文件是否存在
os.makedirs(os.path.join(base_dir,"logs"),exist_ok=True)

#主程序运行
if __name__=="__main__":
    try:
        print("[@] 正在进行 [Log_Rorator] ")
        #调用轮转函数，并接收返回值，输出轮转情况
        val_status,log_status,backup_log=logger.rotate_log(log_dir,MAX_SIZE)
        print(f"{val_status}\n")
        
        #备份程序完成，则进入下一步程序
        #调用内存检查函数，抓取系统当前的 available 内存数值
        print("[@] 正在进行 [Memory_Check] ")
        if log_status is not False:
            success_info,mem_status,available_mem=memory.get_memory_info(log_dir)
        else:
            print("[@] [Memory_Check] 程序未正常进行 \n")
        
    except Exception as e:
        print("** 发生未知异常！**")