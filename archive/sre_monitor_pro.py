from utils import auth
from utils import memory
from collections import Counter
from utils import log
from utils import json
import os

test_auth_log_path=os.path.join(os.getcwd(),"logs","test_auth.log")
auth_log_path=os.path.join("/var","log","auth.log")

#方法: 执行安全审计
def execute_sys_audit(log_name):
    #初始化工作目录
    log_dir=os.path.join(os.getcwd(),'logs')
    log_path=os.path.join(log_dir,log_name)
    
    #解析提取报错日志关键信息
    all_logs=auth.parse_ssh_log(log_path)
    failed_ips=[
        item.get("Ip")
        for item in all_logs
        if "Failed" in item.get("Info","")
    ] 
            
    #空列表判断
    if not failed_ips:
        return False
            
    #抽取出现次数最多的IP
    ip_count=Counter(failed_ips)
    top_ip, count=ip_count.most_common(1)[0]
    
    #获取当前内存使用率
    mem_usage=memory.get_memory_info()
    
    #决策集合(使用列表收集所有警报) and 写入日志
    alert=[]
    usage = mem_usage.get("usage")
    if usage and float(usage) > 90:
        msg=f"内存使用率已达{int(float(usage))}%"
        alert.append(msg)
        log.write_to_log(log.format_alert_text("CRITICAL","high_usage",msg),log_name)
        
    if count>3:
        msg=f"IP: {top_ip},失败次数: {count}"
        alert.append(msg)
        log.write_to_log(log.format_alert_text("CRITICAL","login exception",msg),log_name)
        
    #批量存档history.json   
    for alert_msg in alert:
        json.update_history(alert_msg)
        
    return True
    
if __name__=="__main__":
    print(execute_sys_audit("test_auth.log"))
        