from sre_monitor_hub import get_system_snapshot
from utils import alert
import time
from utils import getTime
from utils import database

#方法: SRE 自动化巡检总线
def start_inspection_loop():
    #检查并创建monitor_log表
    database.init_db_table()
    
    try:
        while True:
            #获取系统状态信息
            data=get_system_snapshot()
            
            #风险状态分析
            res=alert.analyze_snapshot_risk(data)
            
            #逻辑判断
            if alert.has_risk_changed(res.get("level")):
                print({"timestamp":getTime.now(),
                        "status":res.get("level"),
                        "details":res.get("details")})
                print(data)
            else:
                print({"timestamp":getTime.now(),
                    "details":"当前系统状态稳定"})
                
            #信息上传数据库  
            database.extract_and_save(data,res.get("level"))
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n程序已手动结束")
        
    finally:
        #断开数据库连接
        database.close_db()
    
if __name__=="__main__":
    start_inspection_loop()