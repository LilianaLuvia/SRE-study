import utils

#方法: SRE 数据聚合中心
def get_system_snapshot():
    snapshot={
        "hardware":{
            "memory":utils.memory.get_memory_info(),
            "disk":utils.disk.get_disk_usage_report()
        },
        "security":{
            "active_ssh":utils.auth.get_active_ssh_session()
        },
        "process":{
            "cpu_usage":utils.process.get_cpu_usage(),
            "top_process":utils.process.get_processes_cpu_usage()
        }
    }
    return snapshot

if __name__=="__main__":
    utils.json.update_history(get_system_snapshot())