import os
import json
import traceback

config_path=os.path.join("/etc","os-release")
log=["INFO", "ERROR", "INFO", "WARNING", "ERROR", "ERROR"]

#方法：解析debian系统日志
def parse_syslog_line(line: str):
    try:
        info_lst=line.strip().split("|",3)
        if len(info_lst)!=4:
            print("格式不正确喵！")
            return False,None
        clean_info=[item.strip() for item in info_lst]
        timestamp,level,process,message=clean_info
        log={
            "Timestamp":timestamp,
            "Level":level,
            "Process":process,
            "Message":message
        }
        return True,log
    except Exception as e:
        print("出现异常喵！")
        return False,None
        
#方法：日志级别统计数量
def count_log_levels(level_lst:list):
    level_count={}
    for level in level_lst:
        if level in level_count:
            level_count[level]+=1
        else:
            level_count[level]=1
    return level_count
    
#方法：简易读取Linux服务(.conf)，生成配置文件.json
def load_simple_config(config_path):
    json_path=os.path.join(os.getcwd(),"logs","config_record.json")
    try:
        
        #于循环外建立空字典
        config_dir={}
        
        #逐行遍历，节省内存
        with open(config_path,"r") as f:
            for line in f:
                if not line or line.startswith("#"):
                    continue
                else:
                    key,value=line.strip().split("=",1)
                    clean_key=key.strip()
                    clean_value=value.strip().strip('"')
                config_dir[clean_key]=clean_value
            with open(json_path,'w') as f:
                json.dump(config_dir,f,indent=4,ensure_ascii=False)
        return True
    except Exception:
        traceback.print_exc()
        return False
        
if __name__=="__main__":
    parse_syslog_line("2026-04-05 14:00 | ERROR | sshd | Failed password for root from 192.168.1.100  \n")
    count_log_levels(log)
    load_simple_config(config_path)