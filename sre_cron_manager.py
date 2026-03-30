import sre_monitor_v1_2
from datetime import datetime
import os
import time
import traceback

#设置全局变量
base_dir=os.getcwd()
log_dir=os.path.join(base_dir,"logs","health.log")
MAX_SIZE=10*1024
count=0
error_count=0

#主程序运行
if __name__=="__main__":
    try:
        while count<10:
            if error_count<3:
                try:
                    now=datetime.now().strftime("%H:%M:%S")
                    print(f"[{now}] 正在进行第 {count+1} 次循环")
                    success_info,status,available_mem=sre_monitor_v1_2.monitor_memory(log_dir,MAX_SIZE)
                    count+=1
                    if not success_info==False:
                        error_count=0
                    
                except Exception:
                    traceback.print_exc()
                    error_count+=1
            else:
                print(f"** 重试次数超过 {error_count} 次，已自动结束程序 **")
                break
            
            #设置运行间隔
            time.sleep(20)
    except KeyboardInterrupt:
        print("** 程序已手动结束 **")

    finally:
        print(f"** 本次程序已结束 **")
        print(f"** 共执行 {count} 次循环，发生 {error_count} 次错误 **")