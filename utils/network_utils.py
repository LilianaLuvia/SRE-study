import psutil

#方法：查看当前已连接的ip
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
    print(get_active_ssh_session())
