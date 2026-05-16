from prometheus_client import Gauge,start_wsgi_server

cpu_gauge=Gauge('cpu_usage','CPU使用率')
memory_gauge=Gauge('memory_usage','运行内存使用率')
disk_gauge=Gauge('disk_usage','磁盘使用率')
ssh_active_gauge=Gauge('ssh_active_sessions', 'SSH 活跃连接数')
failed_login_gauge=Gauge('ssh_failed_login_count', 'SSH 登录失败总次数')

#方法: 更新Gauge指标
def update_metric(snapshot:dict): 
    cpu_gauge.set(snapshot["process"]["cpu_usage"])
    memory_gauge.set(float(snapshot["hardware"]["memory"]["usage_mem"]))
    disk_gauge.set(float(snapshot["hardware"]["disk"]["usage"]))
    ssh_active_gauge.set(len(snapshot["security"]["active_ssh"]))
    failed_login_gauge.set(sum(snapshot["security"]["frequent_login_error_user"].values()))
    
#方法: 启用HTTP服务,暴露port端口
def start_prometheus_http(port:int=8000):
    start_wsgi_server(port)