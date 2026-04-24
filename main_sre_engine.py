from sre_monitor_hub import get_system_snapshot
from utils import alert
import time
from utils import getTime

#方法: SRE 自动化巡检总线
def start_inspection_loop():
    try:
        while True:
            #获取系统状态信息
            data=get_system_snapshot()
            
            #风险状态分析
            res=alert.analyze_snapshot_risk(data)
            if alert.has_risk_changed(res.get("level")):
                print({"timestamp":getTime.now(),
                        "details":res.get("details")})
                print(data)
            else:
                print({"timestamp":getTime.now(),
                    "details":"当前系统状态稳定"})
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n程序已手动结束")
    
if __name__=="__main__":
    start_inspection_loop()