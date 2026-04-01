import os
import json
import traceback
from datetime import datetime
from modules import log_utils

base_dir=os.getcwd()
log_dir=os.path.join(base_dir,"logs")

#方法：检查memory_history.json是否存在，若不存在则创建json文件
def check_json(log_dir):
    
    try:
        now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        #检查、定义工作目录
        os.makedirs(os.path.join(log_dir),exist_ok=True)
        json_dir=os.path.join(log_dir,"memory_history.json")
        
        #将检查报告写入日志
        if os.path.exists(json_dir):
            log_utils.check_log_exist()
            report=f"""
{"="*50}
{now} [@] [Check_Json_Exist]
Check: OK
{"="*50}\n
                """
            log_utils.write_to_log(report)
        else:
            report=f"\n\nmemory_history.json has been created just now   --- {now}\n\n"
            log_utils.write_to_log(report)
            with open(json_dir,'w') as f:
                json.dump([],f)
    except Exception as e:
        traceback.print_exc()

if __name__=="__main__":
    check_json(log_dir)