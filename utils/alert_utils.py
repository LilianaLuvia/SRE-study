#方法: 状态变迁控制器


#方法: 对sre_monitor_hub.py数据聚合中心的数据进行统一状态分析(专用方法)
def analyze_snapshot_risk(snapshot:dict):
    issues=[]
    memory_usage=float(snapshot["Hardware"]["Memory"]["Usage"])
    disk_usage=float(snapshot["Hardware"]["Disk"]["Usage"])
    active_ssh=snapshot["Security"]["Active_Ssh"]
    
    #硬件检查"Hardware"
    #Meomry Disk
    if memory_usage >90:
        issues.append(f"运行内存占用过高({memory_usage}%)")
    if disk_usage >85:
        issues.append(f"硬盘内存已满({disk_usage}%)")
    
    #安全检查"Security"
    #Active_Ssh
    if len(active_ssh) >=5:
        issues.append(f"当前ssh已连接({active_ssh}个)")
    
    intergrated_info={"Level":None,
                      "Details":issues}
    
    #安全权重分析
    if len(issues)>2 or memory_usage>90:
        intergrated_info["Level"]="CRITICAL"
        return intergrated_info
    elif len(issues)==1:
        intergrated_info["Level"]="WARNING"
        return intergrated_info
    else:
        intergrated_info["Level"]="HEALTHY"
        return intergrated_info
 
if __name__=="__main__":
    pass