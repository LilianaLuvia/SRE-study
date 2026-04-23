import psutil

#方法: 获取磁盘或者某个文件夹下的内存信息
def get_disk_usage_report(path="/"):
    gb_unit=1024**3
    res=psutil.disk_usage(path)
    usage=res.used/res.total
    return {
        "total":f"{res.total/gb_unit:.2f}",
        "used":f"{res.used/gb_unit:.2f}",
        "free":f"{res.free/gb_unit:.2f}",
        "usage":f"{usage*100:.2f}"
    }

if __name__=="__main__":
    print(get_disk_usage_report())