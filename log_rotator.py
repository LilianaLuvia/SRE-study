import os
from datetime import datetime

#设置工作路径
base_dir=os.getcwd()
log_dir=os.path.join(base_dir,"logs","health.log")
Max_Size=3*1024

#方法：对日志文件进行判断大小并备份
def rotate_log(log_dir):
    try:
        
        #检查父目录是否存在
        log_parent_dir=os.path.dirname(log_dir)
        os.makedirs(log_parent_dir,exist_ok=True)
        
        now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if os.path.exists(log_dir):
            
            #判断文件是否大于3kb
            if os.path.getsize(log_dir)>Max_Size:
                print("** 日志文件已大于3kb，准备进行轮转 **")
                timestamp=datetime.now().strftime("%Y%m%d%H%M%S")
                
                #执行os.rename生成备份日志名
                backup_log=f"{log_dir}.{timestamp}.bak"
                os.rename(log_dir,backup_log)
                return True,backup_log
            else:
                size=os.path.getsize(log_dir)
                print(f"文件未超出3kb，当前文件大小：{size} 字节")
                return "Skipped",None
                
        else:
            print("日志文件不存在，已自动创建日志")
            with open(log_dir,'w') as f:
                f.write(f"health.log has been created just now   --- {now}\n")
            return "Initialized",None  
                
    except Exception as e:
        print(f"** 发生异常错误：{e} **")
        return False,None
    
#主程序运行   
if __name__=="__main__":
    status,backup_log=rotate_log(log_dir)
    
    #运行成功则返回备份日志地址
    if status is True:
        print(f"日志已完成备份：{backup_log}")
    elif status == "Skipped":
        print("** 本次日志备份已跳过 **")
    elif status == "Initialized":
        print("日志文件首次创建，已初始化日志")
    else:
        print("日志未能正常备份")
        
    
    