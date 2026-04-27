import utils
import os

#方法: SRE 数据聚合中心
def get_system_snapshot(auth_log_path=None):
    if auth_log_path==None:
        auth_log_path=os.path.join("/var","log","auth.log")
    snapshot={
        "timestamp":utils.getTime.now(),
        "hardware":{
            "memory":utils.memory.get_memory_info(),
            "disk":utils.disk.get_disk_usage_report()
        },
        "security":{
            "status":utils.ip.security_risk_quantification(),
            "frequent_login_error_user":utils.ip.failed_login_user_counter(utils.ip.parse_ssh_log(auth_log_path)),
            "active_ssh":utils.ip.get_active_ssh_session()
        },
        "process":{
            "cpu_usage":utils.process.get_cpu_usage(),
            "top_process":utils.process.get_processes_cpu_usage()
        }
    }
    return snapshot

if __name__=="__main__":
    utils.json.update_history(get_system_snapshot())