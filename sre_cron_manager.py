import sre_monitor_v1_3
from datetime import datetime
import os
import time
import traceback
from modules import memory_utils

#设置全局变量
base_dir=os.getcwd()
log_dir=os.path.join(base_dir,"logs","health.log")
mem_lst=[]
MAX_SIZE=10*1024

def cron_manager(log_dir):
    #定义性能画像变量及统计变量
    avg_mem = 0.0
    highest_mem = 0.0
    lowest_mem = 0.0
    count=0
    error_count=0
    
    #定义返回值字典
    result={
        "success":False,
        "Status":None,
        "Available_Mem":None,
        "Usage%":None
        }
    
    try:
        while count<10:
            if error_count<3:
                try:
                    now=datetime.now().strftime("%H:%M:%S")
                    print(f"[{now}] 正在进行第 {count+1} 次循环")
                    result=sre_monitor_v1_3.monitor_memory(log_dir)
                    count+=1
                    if result.get("success"):
                        mem_lst.append(result.get("Available_Mem",0))
                        error_count=0
                    
                except Exception:
                    traceback.print_exc()
                    error_count+=1
            else:
                print(f"** 重试次数超过 {error_count} 次，已自动结束程序 **")
                break
            
            #设置运行间隔
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("** 程序已手动结束 **")
    
    except Exception:
        print("** 发生未知错误 **")
        traceback.print_exc()

    finally: 
        try:
            total_mem=sum(mem_lst)
            highest_mem=max(mem_lst)
            lowest_mem=min(mem_lst)
            if mem_lst:
                avg_mem=total_mem/len(mem_lst)
            else:
                avg_mem=0
        except Exception:
            print("** 出错了! **")
            traceback.print_exc()
        
        final_report=f"""
{"-"*10} 性能画像报告 {"-"*10}
总巡查次数：{count}
有效样本数：{count-error_count}
平均可用内存：{avg_mem:.2f} Mi
内存波峰：{highest_mem} Mi
内存波谷：{lowest_mem} Mi
{"-"*10} ------------ {"-"*10}
"""
        
        print(f"** 本次程序已结束 **")
        print(f"** 共执行 {count} 次循环，发生 {error_count} 次错误 **")
        print(final_report)
        return None
        
#主程序运行
if __name__=="__main__":
    cron_manager(log_dir)