import pymysql
import time
import os

DB_CONN=None 

DB_HOST=os.environ.get("DB_HOST","127.0.0.1")
DB_USER=os.environ.get("DB_USER","root")
DB_PASSWORD=os.environ.get("DB_PASSWORD","Baiv32992211")
DB_NAME=os.environ.get("DB_NAME","test_database")


#方法: 连接数据库
def connect_to_db():
    count=0
    global DB_CONN
    if DB_CONN is None:
        while DB_CONN is None:
            #连接对象
            try:
                DB_CONN=pymysql.connect(
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    database=DB_NAME
                )
            except Exception:
                count+=1
                print(f"[connect_to_db]: 重连尝试中[{count}]...")
                time.sleep(5)
    return DB_CONN


#方法: 检查并创建表
def init_db_table():
    db_conn=connect_to_db()
    try:
        #sql建表语句
        create_table_sql="""
        CREATE TABLE IF NOT EXISTS monitor_log(
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
            report_time DATETIME COMMENT '报告生成时间',
            mem_usage FLOAT COMMENT '运行内存使用率',
            disk_usage FLOAT COMMENT '磁盘空间使用率',
            cpu_usage FLOAT COMMENT 'CPU占用率',
            security CHAR(10) COMMENT '网络安全状态',
            status CHAR(10) COMMENT '综合状态'
        )
        """
        cursor=db_conn.cursor()
        cursor.execute(create_table_sql)
        
        #提交事务
        db_conn.commit()
    except Exception as e:
        print(f"连接数据库或执行失败: {e}")

#方法: 将系统数据写入数据库
def save_static(time,mem,disk,cpu,level,status):
    global DB_CONN
    try:
        db_conn=connect_to_db()
        save_static_sql="""
        INSERT INTO monitor_log (report_time,mem_usage,disk_usage,cpu_usage,security,status) VALUES (%s,%s,%s,%s,%s,%s)
        """
        cursor=db_conn.cursor()
        cursor.execute(save_static_sql,(time,mem,disk,cpu,level,status))
        db_conn.commit()
    except Exception as e:
        print(f"连接数据库或传入失败: {e}")
        
#方法: 提取snapshot表中的数据并写入数据库
def extract_and_save(snapshot:dict,status):
    timestamp=snapshot["timestamp"]
    mem_usage=float(snapshot["hardware"]["memory"]["usage_mem"])
    disk_usage=float(snapshot["hardware"]["disk"]["usage"])
    cpu_usage=float(snapshot["process"]["cpu_usage"])
    security_status=snapshot["security"]["status"]
    
    save_static(timestamp,mem_usage,disk_usage,cpu_usage,security_status,status)

#方法: 关闭数据库连接
def close_db():
    global DB_CONN
    if DB_CONN:
        DB_CONN.close()
        DB_CONN=None

#方法: 从数据库获取最近count条"CRITICAL"记录并打印
def query_risk_history(count:int=5):
    db_conn=connect_to_db()
    try:
        query_static_sql=f"""
        SELECT * FROM monitor_log WHERE status='CRITICAL' ORDER BY report_time DESC LIMIT {count};
        """
        cursor=db_conn.cursor()
        cursor.execute(query_static_sql)
        rows=cursor.fetchall()
        for row in rows:
            print(f"[{row[1]}] 风险警告 - 运行内存使用率:{row[2]}%, 磁盘空间使用率:{row[3]}%, CPU占用率:{row[4]}%, 网络安全状态:{row[5]}")
    except Exception as e:
        print(f"连接数据库或提取失败: {e}")