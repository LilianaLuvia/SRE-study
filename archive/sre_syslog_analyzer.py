from utils import sys_utils
import traceback

test_logs = [
    "2026-04-07 00:01 | INFO | nginx | worker process started",
    "2026-04-07 00:02 | ERROR | sshd | Failed password for root from 192.168.1.100",
    "2026-04-07 00:03 | ERROR | sshd | Failed password for admin from 192.168.1.101",
    "这是干扰项，应该被跳过喵！", 
    "2026-04-07 00:04 | ERROR | sshd | Failed password for invalid user user1 from 10.0.0.5",
    "2026-04-07 00:05 | WARNING | kernel | Out of memory: Kill process 1234 (python3)",
    "2026-04-07 00:06 | ERROR | sshd | Failed password for root from 192.168.1.100",
    "2026-04-07 00:07 | INFO | systemd | Started Daily Cleanup of Temporary Directories"
]

#方法: 统计系统日志中报错的条目，并收集输出
def analyze_log_stream(raw_line):
    try:
        
        #定义初始变量
        valid_logs=[]
        total_parse=0
        final_dict={}
        
        #解析Stream
        for line in raw_line:
            res,log=sys_utils.parse_syslog_line(line)
            if res:
                valid_logs.append(log)
                total_parse+=1
        
        #统计Stream: 统计各个日志级别数量
        all_valid_level=[logs_level.get("Level") for logs_level in valid_logs]
        level_count=sys_utils.count_log_levels(all_valid_level) 
        
        #设置搜索逻辑(列表推导式) 
        critical_ssh_logs=[logs for logs in valid_logs if logs.get("Process")=="sshd" and logs.get("Level")=="ERROR"]
        
        #返回结果
        final_dict={
            "Total_Parse":total_parse,
            "Level_Stats":level_count,
            "Error_Details":critical_ssh_logs,
            "Is_critical":False
        }
        if len(critical_ssh_logs)>3:
            final_dict["Is_critical"]=True
        return final_dict
    
    except Exception:
        traceback.print_exc()
        
if __name__=="__main__":
    test_dict=analyze_log_stream(test_logs)
    print(test_dict)