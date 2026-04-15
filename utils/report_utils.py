test_example={"192.168.1.100": 15, "172.16.0.5": 3, "10.0.0.1": 8}

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
    print(generate_ascii_bar(test_example))