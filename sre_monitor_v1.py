import os
import subprocess
from datetime import datetime
import log_rotator_v2
import memory_alert_v2_1

#配置环境变量
base_dir=os.getcwd()
log_dir=os.path.join(base_dir,"logs","health.log")
MAX_SIZE=3*1024
FINAL=False

os.makedirs(os.path.join(base_dir,"logs"),exist_ok=True)
log_parent_dir=os.path.dirname(log_dir)

#主程序运行
if __name__=="__main__":
    try:
        print("[@] 正在进行 [Log_Rorator] ")
        #调用轮转函数，并接收返回值，输出轮转情况
        val_status,log_status,backup_log=log_rotator_v2.rotate_log(log_dir,MAX_SIZE)
        print(f"{val_status}\n")
        
        #备份程序完成，则进入下一步程序
        #调用内存检查函数，抓取系统当前的 available 内存数值
        print("[@] 正在进行 [Memory_Check] ")
        if log_status is not False:
            mem_status,available_mem=memory_alert_v2_1.get_memory_info()
            # print(f"当前内存状态：{mem_status},剩余内存为：{available_mem}\n")
            FINAL=True
        else:
            print("[@] [Memory_Check] 程序未正常进行 \n")
            
        #内存检查完成，进入下一步程序
        #格式化report，并写入日志文件
        
        print("[@] 正在进行 [Log_write] ")
        now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if FINAL:
            report=f"""
{"="*50}
{now} [Memory_Check] Status: {mem_status} | Available: {available_mem}
{"="*50}\n
                    """
            get_status,file_size=memory_alert_v2_1.write_to_log(report,log_dir)
            if get_status:
                print("日志已写入\n")
                print(report)
        else:
            print("[@] [Log_write] 程序未正常进行 \n")
        
    except Exception as e:
        print("** 发生未知异常！**")