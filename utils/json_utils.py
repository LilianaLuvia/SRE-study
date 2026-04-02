import os

base_dir=os.getcwd()
log_dir=os.path.join(base_dir,"logs")

#方法：检查memory_history.json是否存在
def check_json_exist():
    result={
        "Success":False,
        "Json_Path":None
    }
    json_path=os.path.join(os.getcwd(),"logs","memory_history.json")
    if not os.path.exists(json_path):  
        return result
    else :
        result.update({
            "Success":False,
            "Json_Path":None
        })
        return result
    
if __name__=="__main__":
    check_json_exist(log_dir)