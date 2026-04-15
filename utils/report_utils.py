test_example={"192.168.1.100": 15, "172.16.0.5": 3, "10.0.0.1": 8}

#方法：生成ip登录错误次数进行图标化
def generate_ascii_bar(stats_dict:dict):
    bar="█"
    max_length=max(stats_dict.values())
    for ip in stats_dict:
        count=stats_dict.get(ip); 
        length=int((count/max_length)*30)
        ascii_bar=f"[{ip:<15}] {bar*length} ({stats_dict.get(ip)})"
        print(ascii_bar)
        
if __name__=="__main__":
    generate_ascii_bar(test_example)