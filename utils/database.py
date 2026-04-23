import pymysql
from utils import getTime
import time

#方法: 连接数据库
def connect_to_db():
    while True:
        #连接对象
        try:
            db_conn=pymysql.connect(
                host="db",
                user="root",
                password="Baiv32992211",
                database="test_database"
            )
            if db_conn:
                break
        except Exception:
            time.sleep(2)
    return db_conn


#方法: 检查并创建表
def init_db_table():
    try:
        db_conn=connect_to_db()
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
        db_conn.close()
    except Exception as e:
        print(f"连接数据库或执行失败: {e}")

#方法: 
def save_static(mem,disk,cpu,level):
    try:
        time=getTime.now()
        db_conn=connect_to_db()
        save_static_sql="""
        INSERT INTO monitor_log (report_time,mem_usage,disk_usage,cpu_usage,status) VALUES (%s,%s,%s,%s,%s)
        """
        cursor=db_conn.cursor()
        cursor.execute(save_static_sql,(time,mem,disk,cpu,level))
        db_conn.commit()
        db_conn.close()
    except Exception as e:
        print(f"连接数据库或传入失败: {e}")