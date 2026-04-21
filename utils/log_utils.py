import os
from datetime import datetime
from utils import auth_utils
import time

#定义环境变量
base_dir=os.getcwd()
log_dir=os.path.join(base_dir,"logs")
log_path=os.path.join(log_dir,"health.log")

# 方法: 检查logs文件夹或日志文件是否存在
def check_log_exist(log_name:str):
    result={
        "success":False,
        "log_path":None
    }
    log_dir=os.path.join(os.getcwd(),"logs")
    log_path=os.path.join(log_dir,log_name)
    if not os.path.exists(log_path):  
        return result
    else :
        result.update({
            "success":True,
            "log_path":log_path
        })
        return result
    
# 方法: 打印日志文件大小
def get_log_size():
    log_size=os.stat(log_path)
    print(f"health.log: {log_size.st_size} 字节")
    return log_size
    
#方法: 将信息写入日志文件
def write_to_log(info,log_name):
    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    final_info=f"{now}\n{info}\n"
    result=check_log_exist(log_name)
    log_path=result.get("Log_Path")
    if result.get("Success") and log_path:
        with open(log_path,'a') as f:
            f.write(info)
        return True
    else:
        print("** 写入失败 **")
        return False
    
#方法: 备份日志文件
def rotate_log(log_path,MAX_SIZE=50*1024):
    
    #定义返回值字典
    result={
        "success":None,
        "status":"日志未能正常备份",
        "backup_log":None
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
                    "success":True,
                    "status":f"日志已完成备份: {backup_log}",
                    "backup_L\log":backup_log
                })
                return result
            else:
                size=os.path.getsize(log_path)
                print(f"文件未超出 {MAX_SIZE} ，当前文件大小: {size} 字节")
                result.update({
                    "success":"Skipped",
                    "status":f"本次日志备份已跳过",
                    "backup_log":None
                })
                return result
                
        else:
            print("** 日志文件不存在，已自动创建日志 **")
            with open(log_path,'w') as f:
                f.write(f"health.log has been created just now   --- {now}\n")
                result.update({
                    "success":"Initialized",
                    "status":"日志文件首次创建，已初始化日志",
                    "backup_log":None
                })
            return result
                
    except Exception as e:
        print(f"** 发生异常错误: {e} **")
        return result

#方法: 构建基础告警标准化模板
def format_alert_text(level,event,detail):
    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{level}] {now} | {event:} | {detail}"

#方法: 实时日志流监听
def follow_logs(log_path:str):
    try:
        with open(log_path,'r') as f:
            f.seek(0,2)
            while True:
                line=f.readline()
                if line:
                    res=auth_utils.parse_ssh_log(line)
                    yield res
                else:
                    time.sleep(0.5)
                    continue           
          
    except KeyboardInterrupt:
        return False

if __name__=="__main__":
    
    # check_log_exist("health.log")
    # get_log_size()
    write_to_log(f"{datetime.now()}这是一次测试日志写入","health.log")
    # result=rotate_log(log_path)
    
    # #运行成功则返回备份日志地址
    # if result.get("Success") is True:
    #     print(f"日志已完成备份: {result.get("Backup_Log")}")
    # elif result.get("Success")=="Skipped":
    #     print("** 本次日志备份已跳过 **")
    # elif result.get("Success")=="Initialized":
    #     print("日志文件首次创建，已初始化日志")
    # else:
    #     print("日志未能正常备份")