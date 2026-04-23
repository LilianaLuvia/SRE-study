from utils import memory
from utils import disk
from utils import auth
from utils import getTime
from datetime import datetime
import os

test_example={"192.168.1.100": 15, "172.16.0.5": 3, "10.0.0.1": 8}

#方法: 获取markdown格式的SRE系统安全与性能审计
def generate_markdown_report(login_failed_dict:dict):
    now=getTime.now()
    mem_report=memory.get_memory_info()
    disk_report=disk.get_disk_usage_report()
    login_failed_report_lines=auth.generate_ascii_bar(login_failed_dict)
    ip_report = ""
    if login_failed_report_lines:
        ip_report="\n".join(login_failed_report_lines)
    
    day=datetime.now().strftime("%Y%m%d")
    log_dirt=os.path.join(os.getcwd(),'logs')
    md_path=f"report_{day}.md" 
    
    total_report=f"""# SRE 系统安全与性能审计
生成时间: {getTime.now()}

|Memory|Static|
|:---:|:---:|
|avaliable_mem|{mem_report.get("available_mem")} Mb|
|usage|{mem_report.get("usage")}%|

|Disk|Static|
|:---:|:---:|
|disk_total|{disk_report.get("total")} Gb|
|disk_used|{disk_report.get("used")} Gb|
|disk_free|{disk_report.get("free")} Gb|
|disk_usage|{disk_report.get("usage")} %|

### ip_count
```text
{ip_report}
```
    """
    
    with open(os.path.join(log_dirt,md_path),'w') as f:
        f.write(total_report)
    
if __name__=="__main__":
    generate_markdown_report(test_example)