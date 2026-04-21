from sre_report_generator import generate_markdown_report
from utils import ip_utils
import time
import os

test_auth_log_path=os.path.join(os.getcwd(),"logs","test_auth.log")

#方法: 控制程序自动化运行
def start_watchdog(interval:int,test_auth_log_path:str):
    try:
        count=1
        while 1:
            print(f"正在进行第 {count} 次巡检")
            parse_result=ip_utils.parse_ssh_log(test_auth_log_path)
            ip_count=ip_utils.ip_counter(parse_result)
            generate_markdown_report(ip_count)
            count+=1
            time.sleep(interval)
        
    except KeyboardInterrupt:
        print("\n巡检结束")
        
if __name__=="__main__":
    start_watchdog(3,test_auth_log_path)