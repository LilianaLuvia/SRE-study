import re
import os

test_auth_log_path=os.path.join(os.getcwd(),"logs","test_auth.log")

#方法：正则表达式截取ip登录信息
def parse_ssh_log(auth_log_path):
    regex_pattern=r"]: (?P<Info>.*?) for (?P<User>.*?) from (?P<Ip>\d+\.\d+\.\d+\.\d+) port (?P<Port>\d+)"
    parse_result=[]
    
    #提取日志文件内容
    with open(test_auth_log_path,'r') as f:
        for line in f:
            clean_line=line
            
            #解析日志行
            match=re.search(regex_pattern,clean_line)
            if match:
                parse_result.append(match.groupdict())

    return parse_result

if __name__=="__main__":
    result=parse_ssh_log(test_auth_log_path)
    print(result)