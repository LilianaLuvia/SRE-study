import re
import os
from collections import Counter
from typing import Iterable
import psutil

test_auth_log_path=os.path.join(os.getcwd(),"logs","test_auth.log")

#方法: 正则表达式截取ip登录信息
def parse_ssh_log(source):
    regex_pattern=r"]: (?P<Info>.*?) for (?P<User>.*?) from (?P<Ip>\d+\.\d+\.\d+\.\d+) port (?P<Port>\d+)"
    parse_result=[]
    
   #内部方法: 统一不同输入源
    def handle_stream(source):
        if isinstance(source,str):
            if os.path.exists(source):
                with open(source,'r') as f:
                    for line in f:
                        yield line.strip()
            else:
                yield source.strip()
        elif isinstance(source,list):
            for line in source:
                yield line
        else:
            raise ValueError("[ parse_ssh_log ] : 传入数据类型错误!")
        
    #统一进行解析
    for i in handle_stream(source):
        match=re.search(regex_pattern,i)
        if match:
            yield match.groupdict()

#方法: 统计各个ip的出现次数，返回从大到小排序,传入count以指定传回前n项
def ip_counter(parse_result:Iterable,count:int=0):
    counter_ip=Counter(item["Ip"] for item in parse_result)
    return dict(counter_ip.most_common(count if count>0 else None))

#方法: 生成ip登录错误次数进行图标化
def generate_ascii_bar(stats_dict:dict,reverse: bool=True):
    bar="█"
    ascii_bar=[]
    if stats_dict:
        max_length=max(stats_dict.values())
        sorted_dict=sorted(stats_dict.items(),key=lambda item: item[1],reverse=reverse)
        for ip,count in sorted_dict: 
            length=int((count/max_length)*30)
            ascii_bar.append(f"[{ip:<15}] {bar*length} ({count})")
        return ascii_bar
    
    else:
        print("导入了空字典喵！")
        return None
    
#方法: 查看当前远程连接中已连接的ip
def get_active_ssh_session():
    total=[]
    connection=psutil.net_connections("inet")
    for connect in connection:
        if connect.status=="ESTABLISHED" and connect.raddr and connect.raddr.port==22:
            total.append({"Remote_Ip":connect.raddr.ip,
                          "Remote_Port":connect.raddr.port,
                          "Status":connect.status})
    return total
    
if __name__=="__main__":
    ip_count=ip_counter(parse_ssh_log(test_auth_log_path))
    print(ip_count)
    print(generate_ascii_bar(ip_count))