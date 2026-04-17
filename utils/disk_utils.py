import shutil

#方法：获取磁盘或者某个文件夹下的内存信息
def get_disk_usage_report(path="/"):
    gb_unit=1024**3
    res=shutil.disk_usage(path)
    usage=res.used/res.total
    return {
        "Total":f"{res.total/gb_unit:.2f}",
        "Used":f"{res.used/gb_unit:.2f}",
        "Free":f"{res.free/gb_unit:.2f}",
        "Usage":f"{usage*100:.2f}",
        "Status":"HEALTHY" if usage<0.85 else "DANGER"
    }

if __name__=="__main__":
    print(get_disk_usage_report())