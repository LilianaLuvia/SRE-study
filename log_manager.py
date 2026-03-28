import os
from datetime import datetime

#查看当前工作路径
print(os.getcwd())

#初始化需求工作路径，把路径定义成变量，方便以后修改
base_dir=os.path.join(os.getcwd(),"logs")

#已有日志文件基础上，写入文件内容
#若文件不存在则创建一个并写入当前时间
file_name="health.log"
full_f_name=os.path.join(base_dir,"health.log")

# 方法：检查文件是否存在，若不存在则创建文件
def check_Log_Exist():
    time=datetime.now()
    if not os.path.exists(full_f_name) :
        with open(full_f_name,"w") as f :
            f.write(f"health.log has been created just now   --- {time}\n")
    else :
        with open(full_f_name,"a") as f :
            f.write(f"System Check: OK   --- {time}\n")

# 方法：打印health.log文件大小
def get_Log_Size():
    log_info=os.stat(full_f_name)
    print(f"health.log: {log_info.st_size} 字节")

if __name__=="__main__":
    check_Log_Exist()
    get_Log_Size()
    
#读取文件内容并打印，确认写入成功
with open(full_f_name,"r") as f :
    content=f.read()
    print(content)