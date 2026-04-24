import pymysql
from utils import getTime
import time

DB_CONN=None 

#方法: 连接数据库
def connect_to_db():
    global DB_CONN
    if DB_CONN is None:
        while True:
            #连接对象
            try:
                DB_CONN=pymysql.connect(
                    host="db",
                    user="root",
                    password="Baiv32992211",
                    database="test_database"
                )
                if DB_CONN:
                    break
            except Exception:
                print("[connect_to_db]: 重连尝试中...")
                time.sleep(2)
    return DB_CONN


#方法: 检查并创建表
def init_db_table():
    db_conn=connect_to_db()
    try:
        create_table_sql="""
        CREATE TABLE IF NOT EXISTS monitor_log(
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
            report_time DATETIME COMMENT '报告生成时间',
            mem_usage FLOAT COMMENT '运行内存使用率',
            disk_usage FLOAT COMMENT '磁盘空间使用率',
            cpu_usage FLOAT COMMENT 'CPU占用率',
            status CHAR(10) COMMENT '系统状态'
        )
        """
        cursor=db_conn.cursor()
        cursor.execute(create_table_sql)
        db_conn.commit()
        print("表创建成功")
    except Exception as e:
        print(f"连接数据库或执行失败: {e}")

#方法: 将系统数据写入数据库
def save_static(time,mem,disk,cpu,level):
    global DB_CONN
    try:
        db_conn=connect_to_db()
        save_static_sql="""
        INSERT INTO monitor_log (report_time,mem_usage,disk_usage,cpu_usage,status) VALUES (%s,%s,%s,%s,%s)
        """
        cursor=db_conn.cursor()
        cursor.execute(save_static_sql,(time,mem,disk,cpu,level))
        db_conn.commit()
    except Exception as e:
        print(f"连接数据库或传入失败: {e}")
        
#方法: 提取snapshot表中的数据
def extract_and_save(snapshot:dict):
    timestamp=snapshot["timestamp"]
    mem_usage=float(snapshot["hardware"]["memory"]["usage_mem"])
    disk_usage=float(snapshot["hardware"]["disk"]["usage"])
    cpu_usage=float(snapshot["process"]["cpu_usage"])
    security_status=snapshot["security"]["status"]
    save_static(timestamp,mem_usage,disk_usage,cpu_usage,security_status)

#方法: 关闭数据库连接
def close_db():
    global DB_CONN
    if DB_CONN:
        DB_CONN.close()
        DB_CONN=None
        