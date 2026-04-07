from utils import regex_utils
from utils import memory_utils
from collections import Counter
from utils import log_utils
from utils import json_utils

raw_auth_logs = [
    "Apr 7 10:00:01 debian sshd[111]: Accepted password for siqi from 192.168.1.5 port 22 ssh2",
    "Apr 7 10:01:05 debian sshd[123]: Failed password for root from 192.168.1.100 port 56789 ssh2",
    "Apr 7 10:01:08 debian sshd[124]: Failed password for root from 192.168.1.100 port 56790 ssh2",
    "Apr 7 10:01:12 debian sshd[125]: Failed password for invalid user admin from 192.168.1.101 port 43210 ssh2",
    "Apr 7 10:01:15 debian sshd[126]: Failed password for root from 192.168.1.100 port 56791 ssh2",
    "Apr 7 10:02:01 debian systemd[1]: Starting Daily Cleanup of Temporary Directories...",
    "Apr 7 10:03:45 debian sshd[127]: Failed password for invalid user guest from 172.16.0.5 port 33221 ssh2",
    "Apr 7 10:03:50 debian sshd[128]: Failed password for root from 192.168.1.100 port 56792 ssh2",
    "Apr 7 10:04:10 debian kernel: [1234.56] Out of memory: Kill process 999 (malicious_bin)",
    "Apr 7 10:05:00 debian sshd[129]: Failed password for root from 192.168.1.100 port 56793 ssh2"
]

#方法：执行安全审计
def execute_sys_audit(raw_auth_logs):
    
    #解析提取报错日志关键信息
    failed_ips=[
        parse.get("Ip")
        for line in raw_auth_logs
        if (parse:=regex_utils.parse_ssh_log(line)) and "Failed" in line
    ]
            
    #空列表判断
    if not failed_ips:
        return
            
    #抽取出现次数最多的IP
    ip_count=Counter(failed_ips)
    top_ip, count=ip_count.most_common(1)[0]
    
    #获取当前内存使用率
    mem_usage=memory_utils.get_memory_info()
    
    #决策集合(使用列表收集所有警报) and 写入日志
    alert=[]
    if float(mem_usage.get("Usage"))>90:
        msg=f"内存使用率已达{int(mem_usage.get("Usage"))}%"
        alert.append(msg)
        log_utils.write_to_log(log_utils.format_alert_text("CRITICAL","High_Usage",msg))
        
    if count>3:
        msg=f"IP: {top_ip},失败次数: {count}"
        alert.append(msg)
        log_utils.write_to_log(log_utils.format_alert_text("CRITICAL","Login Exception",msg))
        
    #批量存档history.json   
    for alert_msg in alert:
        json_utils.update_history(alert_msg)
    
if __name__=="__main__":
    execute_sys_audit(raw_auth_logs)
        