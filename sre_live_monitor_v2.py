from collections import Counter
import sre_live_tailer
from utils import ip_utils
import sre_report_generator
import time

#方法：多维监控
def run_intergrated_monitor(log_name:str):
    ip_attack_count=Counter()
    last_time=0
    
    #由迭代器follow_logs驱动流程,follow_logs每产生一行就进行完整流程一次
    for new_res in sre_live_tailer.follow_logs(log_name):
        for ip_res in new_res:
            target_ip=ip_res.get("Ip")
            ip_attack_count.update([target_ip])

        current_time=time.time()
        if current_time-last_time>10 and ip_attack_count:
            sre_report_generator.generate_markdown_report(ip_attack_count)
            last_time=current_time
        

if __name__=="__main__":
    print(run_intergrated_monitor("test_auth.log"))
        