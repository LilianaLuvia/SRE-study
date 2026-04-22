from sre_monitor_hub import get_system_snapshot
from utils import alert_u
import time
from utils import get_time

#方法: SRE 自动化巡检总线
def start_inspection_loop():
    try:
        while True:
            data=get_system_snapshot()
            res=alert_u.analyze_snapshot_risk(data)
            if alert_u.has_risk_changed(res.get("level")):
                print({"timestamp":get_time(),
                        "details":res.get("details")})
                print(data)
            else:
                print({"timestamp":get_time(),
                    "details":"当前系统状态稳定"})
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n程序已手动结束")
    
if __name__=="__main__":
    start_inspection_loop()