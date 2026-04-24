last_level="HEALTHY"

#方法: 状态变迁控制器
def has_risk_changed(new_level):
    global last_level
    
    #状态发生改变
    if new_level!=last_level:
        last_level=new_level
        return True
    
    #状态未发生改变
    if new_level in ("CRITICAL", "WARNING"):
        return True
    
    return False

#方法: 对sre_monitor_hub.py数据聚合中心的数据进行统一状态分析(专用方法)
def analyze_snapshot_risk(snapshot:dict):
    issues=[]
    memory_usage=float(snapshot["hardware"]["memory"]["usage_mem"])
    disk_usage=float(snapshot["hardware"]["disk"]["usage"])
    cpu_usage=float(snapshot["process"]["cpu_usage"])
    failed_login_user=snapshot["security"]["frequent_login_error_user"]
    active_ssh=snapshot["security"]["active_ssh"]
    
    #硬件检查"hardware"
    #meomry disk
    if memory_usage >93:
        issues.append(f"运行内存使用率过高({memory_usage}%)") 
    if disk_usage >93:
        issues.append(f"磁盘内存已满({disk_usage}%)")
        
    #进程检查"process"
    if cpu_usage>93:
        issues.append(f"CPU负载过高({cpu_usage})")
        
    #安全检查"security"
    #frequent_login_error_user
    for user,count in failed_login_user.items():
        if count>20:            
            issues.append(f"当前存在疑似爆破登录攻击({user}),失败次数 {count}")
        elif count>10:
            issues.append(f"当前存在高频登录失败({user}),失败次数 {count}")
            
    #active_hsh
    if len(active_ssh) >=5:
        issues.append(f"当前ssh已连接({len(active_ssh)}个)")
    
    intergrated_info={"level":None,
                    "details":issues}
    
    #安全权重分析
    if len(issues)>2 or memory_usage>93 or cpu_usage>93:
        intergrated_info["level"]="CRITICAL"
        return intergrated_info
    elif len(issues)==1:
        intergrated_info["level"]="WARNING"
        return intergrated_info
    else:
        intergrated_info["level"]="HEALTHY"
        return intergrated_info

if __name__=="__main__":
    pass