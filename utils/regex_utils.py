import re

test_text="Apr 7 00:02:01 debian sshd[1234]: Failed password for invalid user siliana from 192.168.1.100 port 54321 ssh2"

def parse_ssh_log(line):
    regex_pattern=r"]: (?P<Info>.*?) for (?P<User>.*?) from (?P<Ip>\d+\.\d+\.\d+\.\d+) port (?P<Port>\d+)"
    match=re.search(regex_pattern,line)
    if match:     
        return match.groupdict()
    else:
        return None

if __name__=="__main__":
    result=parse_ssh_log(test_text)
    print(result)