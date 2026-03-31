import os
from datetime import datetime

#定义环境变量
base_dir=os.getcwd()
log_dir=os.path.join(base_dir,"logs","health.log")
MAX_SIZE=10*1024

# 方法：检查logs文件夹或日志文件是否存在，若不存在则创建logs文件夹或日志文件
def check_log_exist():
    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    os.makedirs(os.path.join(base_dir,"logs"),exist_ok=True)
    
    if os.path.exists(log_dir) :
        report=f"""
{"="*50}
{now} [@] [Check_Log_Exist] Check: OK
{"="*50}\n
                """
        with open(log_dir,"a") as f :
            f.write(report)
        print(report)
        
    else :
        with open(log_dir,"w") as f :
            f.write(f"health.log has been created just now   --- {now}\n\n")

# 方法：打印日志文件大小
def get_log_size():
    log_info=os.stat(log_dir)
    print(f"health.log: {log_info.st_size} 字节")
    
#方法：备份日志文件
def rotate_log(log_dir,MAX_SIZE):
    
    #定义返回值字典
    result={
        "success":None,
        "Status":None,
        "Backup_Log":None
    }
    try:
        
        #检查父目录是否存在
        os.makedirs(os.path.dirname(log_dir),exist_ok=True)
        
        now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if os.path.exists(log_dir):
            
            #判断文件是否大于 MAX_SIZE 字节
            if os.path.getsize(log_dir)>MAX_SIZE:
                print(f"** 日志文件已大于 {MAX_SIZE} 字节，准备进行轮转 **")
                timestamp=datetime.now().strftime("%Y%m%d-%H%M%S")
                
                #执行os.rename生成备份日志名
                backup_log=f"{log_dir}.{timestamp}.bak"
                os.rename(log_dir,backup_log)
                result.update({
                    "success":True,
                    "Status":f"日志已完成备份：{backup_log}",
                    "Backup_Log":backup_log
                })
                return result
            else:
                size=os.path.getsize(log_dir)
                print(f"文件未超出 {MAX_SIZE} ，当前文件大小：{size} 字节")
                result.update({
                    "success":"Skipped",
                    "Status":f"本次日志备份已跳过，当前文件大小：{size} 字节",
                    "Backup_Log":None
                })
                return result
                
        else:
            print("日志文件不存在，已自动创建日志")
            with open(log_dir,'w') as f:
                f.write(f"health.log has been created just now   --- {now}\n")
                result.update({
                    "success":"Initialized",
                    "Status":"日志文件首次创建，已初始化日志",
                    "Backup_Log":None
                })
            return "Initialized","日志文件首次创建，已初始化日志",None
                
    except Exception as e:
        print(f"** 发生异常错误：{e} **")
        return False,"日志未能正常备份",None

if __name__=="__main__":
    
    check_log_exist()
    get_log_size()
    val_status,status,backup_log=rotate_log(log_dir,MAX_SIZE)
    
    #运行成功则返回备份日志地址
    if status is True:
        print(f"日志已完成备份：{backup_log}")
    elif status == "Skipped":
        print("** 本次日志备份已跳过 **")
    elif status == "Initialized":
        print("日志文件首次创建，已初始化日志")
    else:
        print("日志未能正常备份")