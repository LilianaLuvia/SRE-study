from utils import memory_utils
from utils import ip_utils
from utils import get_time
from datetime import datetime
import os

test_example={"192.168.1.100": 15, "172.16.0.5": 3, "10.0.0.1": 8}

#方法：获取markdown格式的SRE系统安全与性能审计日报
def generate_markdown_report(ip_dict:dict):
    now=get_time()
    mem_report=memory_utils.get_memory_info()
    ip_report_lines=ip_utils.generate_ascii_bar(ip_dict)
    ip_report="\n".join(ip_report_lines)
    
    day=datetime.now().strftime("%Y%m%d")
    log_dirt=os.path.join(os.getcwd(),'logs')
    md_path=f"report_{day}.md"
    
    total_report=f"""# SRE 系统安全与性能审计日报
生成时间：{now}

|Project|Static|
|:---:|:---:|
|Avaliable_Mem|{mem_report.get("Available_Mem")} Mb|
|Usage|{mem_report.get("Usage")}%|
```text
{ip_report}
```
    """
    
    with open(os.path.join(log_dirt,md_path),'w') as f:
        f.write(total_report)
    
if __name__=="__main__":
    generate_markdown_report(test_example)