import json
import os
import traceback

config_path=os.path.join("/etc","os-release")

#方法：简易读取Linux服务(.conf)，生成配置文件.json
def load_simple_config(config_path):
    json_path=os.path.join(os.getcwd(),"logs","config_record.json")
    try:
        
        #于循环外建立空字典
        config_dir={}
        
        #逐行遍历，节省内存
        with open(config_path,"r") as f:
            for line in f:
                if not line or line.startswith("#"):
                    continue
                else:
                    key,value=line.strip().split("=",1)
                    clean_key=key.strip()
                    clean_value=value.strip().strip('"')
                config_dir[f"{clean_key}"]=clean_value
            with open(json_path,'a') as f:
                json.dump(config_dir,f,indent=4,ensure_ascii=False)
    except Exception:
        traceback.print_exc()
            
if __name__=="__main__":
    load_simple_config(config_path)