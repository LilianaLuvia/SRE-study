import re
import os
from collections import Counter

test_auth_log_path=os.path.join(os.getcwd(),"logs","test_auth.log")

#方法：正则表达式截取ip登录信息
def parse_ssh_log(auth_log_path):
    regex_pattern=r"]: (?P<Info>.*?) for (?P<User>.*?) from (?P<Ip>\d+\.\d+\.\d+\.\d+) port (?P<Port>\d+)"
    parse_result=[]
    
    #提取日志文件内容
    with open(auth_log_path,'r') as f:
        for line in f:
            clean_line=line
            
            #解析日志行
            match=re.search(regex_pattern,clean_line)
            if match:
                parse_result.append(match.groupdict())

    return parse_result

#方法：统计各个ip的出现次数
def ip_counter(parse_result:list):
    return Counter(item["Ip"] for item in parse_result)

#方法：生成ip登录错误次数进行图标化
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
    
if __name__=="__main__":
    print(generate_ascii_bar(test_auth_log_path))