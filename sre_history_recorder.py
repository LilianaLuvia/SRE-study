import json
import os
import traceback
from datetime import datetime

json_path=os.path.join(os.getcwd(),"logs","memory_history.json")

def update_history(json_path,new_value,max_limit=10):
    try:
        now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        #检查json文件存在与否,否则创建新的json
        if os.path.exists(json_path):
            with open(json_path,'r',encoding="UTF-8") as f:      
                now_list=json.load(f)
        else:
            now_list=[]
        #创建新字典
        new_dir={"timestamp":now,
            "value":f"{new_value}",
            }
        
        #从列表头添加元素
        now_list.insert(0,new_dir)
        
        #列表长度截断
        now_list=now_list[:max_limit]
        
        #将列表写入Json
        with open(json_path,'w') as f:
            json.dump(now_list,f,indent=4,ensure_ascii=False)
        
        return True
    except Exception:
        traceback.print_exc()
        return False
    
if __name__=="__main__":
    update_history(json_path,"测试信息")    