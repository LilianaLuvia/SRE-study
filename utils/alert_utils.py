#方法：对sre_monitor_hub.py数据聚合中心的数据进行统一状态分析(专用方法)
def analyze_snapshot_risk(snapshot:dict):
    issus=[]
    memory_usage=float(snapshot["Hardware"]["Memory"]["Usage"])
    disk_usage=float(snapshot["Hardware"]["Disk"]["Usage"])
    active_ssh=snapshot["Security"]["Active_Ssh"]
    
    #硬件检查"Hardware"
    #Meomry Disk
    if memory_usage >90:
        issus.append(f"运行内存占用过高({memory_usage}%)")
    if disk_usage >85:
        issus.append(f"硬盘内存已满({disk_usage}%)")
    
    #安全检查"Security"
    #Active_Ssh
    if len(active_ssh) >=5:
        issus.append(f"当前ssh已连接({active_ssh}个)")
        
    return issus
        
if __name__=="__main__":
    pass