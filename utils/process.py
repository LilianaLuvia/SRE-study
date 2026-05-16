import psutil
from datetime import datetime
from utils import database
import time

#方法: 遍历系统当前运行的所有进程，获取进程的使用信息
def get_processes_cpu_usage(count=5):
    total_process=[]
    #预热: 触发所有进程的第一次采样
    for p in psutil.process_iter(attrs=["cpu_percent"]):
        pass
    time.sleep(0.7)
    
    #正式采样
    for process in psutil.process_iter(attrs=['pid','name','cpu_percent','create_time']):
        if process:
            try:
                create_time=process.info.get('create_time')
                if create_time:
                    timestamp=datetime.fromtimestamp(create_time).strftime("%Y-%m-%d %H:%M:%S")
                    process.info.update({'create_time':timestamp})
                    total_process.append(process.info)
                
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    total_process.sort(key=lambda x:x['cpu_percent'],reverse=True)
    return total_process[:count]

#方法: 获取CPU使用率
def get_cpu_usage():
    return psutil.cpu_percent(interval=0.7)

#方法: 从数据库获取最近count条CPU使用率,计算平均值
def calculate_moving_avg_cpu(count:int=10):
    db_conn=database.connect_to_db()
    calculate_moving_avg_cpu_sql=f"""
    SELECT AVG(cpu_usage) FROM (SELECT cpu_usage FROM monitor_log ORDER BY id DESC LIMIT {count}) as temp;
    """
    cursor=db_conn.cursor()
    cursor.execute(calculate_moving_avg_cpu_sql)
    result=cursor.fetchone()
    cursor.close()
    if result and result[0] is not None:
        return result[0]
    return 0.0
    
if __name__=="__main__":
    print(get_processes_cpu_usage())