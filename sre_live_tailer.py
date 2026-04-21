import os
from utils import ip_utils
import time

test_auth_log_path=os.path.join(os.getcwd(),"logs","test_auth.log")

#方法: 实时日志流监听
def follow_logs(log_name:str):
    log_path=os.path.join(os.getcwd(),"logs",f"{log_name}")
    try:
        with open(log_path,'r') as f:
            f.seek(0,2)
            while True:
                line=f.readline()
                if line:
                    res=ip_utils.parse_ssh_log(line)
                    yield res
                else:
                    time.sleep(0.5)
                    continue           
          
    except KeyboardInterrupt:
        return False

if __name__=="__main__":
    follow_logs(test_auth_log_path)