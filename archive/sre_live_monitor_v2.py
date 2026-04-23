from collections import Counter
from utils import log
import archive.sre_report_generator as sre_report_generator
import time
import os

auth_log_path=os.path.join("/var","log","auth.log")

#方法: 多维监控
def run_intergrated_monitor(log_path:str):
    login_attack_count=Counter()
    last_time=0
    
    #由迭代器follow_logs驱动流程,follow_logs每产生一行就进行完整流程一次
    for new_res in log.follow_logs(log_path):
        for res in new_res:
            failed_user=res.get("who")
            login_attack_count.update([failed_user])

        current_time=time.time()
        if current_time-last_time>10 and login_attack_count:
            sre_report_generator.generate_markdown_report(login_attack_count)
            last_time=current_time
        

if __name__=="__main__":
    print(run_intergrated_monitor(auth_log_path))
        