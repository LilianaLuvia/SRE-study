import utils

#方法: SRE 数据聚合中心
def get_system_snapshot():
    snapshot={
        "hardware":{
            "memory":utils.memory_u.get_memory_info(),
            "disk":utils.disk_u.get_disk_usage_report()
        },
        "security":{
            "active_ssh":utils.auth_u.get_active_ssh_session()
        },
        "process":{
            "top_process":utils.process_u.get_cpu_processes()
        }
    }
    return snapshot

if __name__=="__main__":
    utils.json_u.update_history(get_system_snapshot())