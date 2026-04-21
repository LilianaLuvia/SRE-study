import os
import json
import traceback
from datetime import datetime

base_dir=os.getcwd()

#方法: 检查memory_history.json是否存在
def check_json_exist():
    json_path=os.path.join(os.getcwd(),"logs","history.json")
    if not os.path.exists(json_path):  
        return False
    else :
        return True
    
#方法: 向history.json添加信息,可一次性自定义history.json文件位置
def update_history(new_value,json_path=None):
    
    #默认路径处理: 避免在函数定义时计算动态路径
    if json_path is None:
        json_path=os.path.join(os.getcwd(),"logs","history.json")
        
    #定义列表长度上限   
    max_limit=10
    
    try:
        now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        #检查json文件存在与否,否则创建新的json
        if os.path.exists(json_path):
            with open(json_path,'r',encoding="UTF-8") as f:      
                now_list=json.load(f)
        else:
            now_list=[]
        #创建新字典
        new_dir={"Timestamp":now,
            "Info":new_value,
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
    check_json_exist()
    update_history("测试信息")  