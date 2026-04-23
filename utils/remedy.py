def get_remedy_suggestion(issue_list:list):
    strategy={
        "运行内存":"advice: 检查并关闭僵尸进程或内存泄漏应用",
        "磁盘内存":"advice: 删除旧日志文件或临时缓存",
        "CPU负载":"advice: 检查高CPU占用率进程,若为正常业务,则考虑扩容,否则kill",
        "ip高频登录":"advice: 将高频登录加入黑名单或临时封禁",
        "ssh":"advice: 核对登录白名单"
    }
    return [strategy.get(key,"advice: 暂无可用建议,请人工检查") for key in strategy.keys() if key in issue_list]