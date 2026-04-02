import os
from datetime import datetime

#定义环境变量
base_dir=os.getcwd()
log_dir=os.path.join(base_dir,"logs")
log_path=os.path.join(log_dir,"health.log")

# 方法：检查logs文件夹或日志文件是否存在
def check_log_exist():
    result={
        "Success":False,
        "Log_Path":None
    }
    log_path=os.path.join(os.getcwd(),"logs","health.log")
    if not os.path.exists(log_path):  
        return result
    else :
        result.update({
            "Success":False,
            "Log_path":None
        })
        return result
    
# 方法：打印日志文件大小
def get_log_size():
    log_size=os.stat(log_path)
    print(f"health.log: {log_size.st_size} 字节")
    return log_size
    
#方法：将信息写入日志文件
def write_to_log(info):
    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    final_info=f"{now}\n{info}\n"
    result=check_log_exist()
    if result.get("Success"):
        with open(result.get("Log_Path"),'a') as f:
            f.write(final_info)
        return True
    else:
        print("** 写入失败 **")
        return False
    
#方法：备份日志文件
def rotate_log(log_path,MAX_SIZE=50*1024):
    
    #定义返回值字典
    result={
        "Success":None,
        "Status":"日志未能正常备份",
        "Backup_Log":None
    }
    try:    
        now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if os.path.exists(log_path):
            
            #判断文件是否大于 MAX_SIZE 字节
            if os.path.getsize(log_path)>MAX_SIZE:
                print(f"""
** 日志文件已大于 {MAX_SIZE} 字节，准备进行轮转 **""")
                timestamp=datetime.now().strftime("%Y%m%d-%H%M%S")
                
                #执行os.rename生成备份日志名
                backup_log=f"{log_path}.{timestamp}.bak"
                os.rename(log_path,backup_log)
                result.update({
                    "Success":True,
                    "Status":f"日志已完成备份：{backup_log}",
                    "Backup_Log":backup_log
                })
                return result
            else:
                size=os.path.getsize(log_path)
                print(f"文件未超出 {MAX_SIZE} ，当前文件大小：{size} 字节")
                result.update({
                    "Success":"Skipped",
                    "Status":f"本次日志备份已跳过",
                    "Backup_Log":None
                })
                return result
                
        else:
            print("** 日志文件不存在，已自动创建日志 **")
            with open(log_path,'w') as f:
                f.write(f"health.log has been created just now   --- {now}\n")
                result.update({
                    "Success":"Initialized",
                    "Status":"日志文件首次创建，已初始化日志",
                    "Backup_Log":None
                })
            return result
                
    except Exception as e:
        print(f"** 发生异常错误：{e} **")
        return result

if __name__=="__main__":
    
    check_log_exist()
    get_log_size()
    write_to_log("这是一次测试日志写入")
    result=rotate_log(log_path)
    
    #运行成功则返回备份日志地址
    if result.get("Success") is True:
        print(f"日志已完成备份：{result.get("Backup_Log")}")
    elif result.get("Success")=="Skipped":
        print("** 本次日志备份已跳过 **")
    elif result.get("Success")=="Initialized":
        print("日志文件首次创建，已初始化日志")
    else:
        print("日志未能正常备份")