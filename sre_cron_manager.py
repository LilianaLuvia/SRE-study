from modules import memory_utils
from datetime import datetime
import os
import time
import traceback

#设置全局变量
base_dir=os.getcwd()
log_path=os.path.join(base_dir,"logs","health.log")

def cron_manager(log_path):
    
    #定义方法内变量
    mem_lst=[]
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
                    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"{now} 正在进行第 {count+1} 次循环")
                    result=memory_utils.get_memory_info(log_path)
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
                
            final_report=f"""
{"-"*10} 性能画像报告 {"-"*10}
总巡查次数：{count}
有效样本数：{count-error_count}
平均可用内存：{avg_mem:.2f} Mi
内存波峰：{highest_mem} Mi
内存波谷：{lowest_mem} Mi
{"-"*10} ------------ {"-"*10}
"""
        except Exception:
            print("** 出错了! **")
            traceback.print_exc()
        
        
        print(f"** 本次程序已结束 **")
        print(f"** 共执行 {count} 次循环，发生 {error_count} 次错误 **")
        print(final_report)
        
        return result
        
#主程序运行
if __name__=="__main__":
    cron_manager(log_path)