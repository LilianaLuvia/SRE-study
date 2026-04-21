import utils

#方法: SRE 数据聚合中心
def get_system_snapshot():
    snapshot={
        "Hardware":{
            "Memory":utils.memory_u.get_memory_info(),
            "Disk":utils.disk_u.get_disk_usage_report()
        },
        "Security":{
            "Active_Ssh":utils.ip_u.get_active_ssh_session()
        },
        "Process":{
            "Top_Process":utils.process_u.get_cpu_processes()
        }
    }
    return snapshot

if __name__=="__main__":
    utils.json_u.update_history(get_system_snapshot())