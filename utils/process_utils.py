import psutil
from collections import Counter
from datetime import datetime

#方法: 遍历系统当前运行的所有进程，获取进程的使用信息
def get_cpu_processes(count=5):
    total_process=[]
    for process in psutil.process_iter(attrs=['pid','name','cpu_percent','create_time']):
        if process:
            try:
                time=process.info.get('create_time')
                if time:
                    timestamp=datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")
                    process.info.update({'create_time':timestamp})
                    total_process.append(process.info)
                
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    total_process.sort(key=lambda x:x['cpu_percent'],reverse=True)
    return total_process[:count]

if __name__=="__main__":
    print(get_cpu_processes())