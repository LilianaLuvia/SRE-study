from dotenv import load_dotenv
load_dotenv()
import pandas as pd
from utils.database import connect_to_db,close_db

# 连接数据库拉取最近limit条记录,返回DateFrame
def load_from_db(limit:int=500):
    db_conn=connect_to_db()
    
    try:
        load_from_db_sql=f"""
        SELECT report_time,mem_usage,disk_usage,cpu_usage,security,status FROM monitor_log ORDER BY report_time DESC LIMIT 500
        """
        # 执行SQL语句并获取数据表格
        df=pd.read_sql(load_from_db_sql,db_conn)
        close_db()
        
        return df
        
    except Exception as e:
        print(f"发生未知错误: {e}")

# 整理从数据库拉取的数据,为后续开发做准备    
def prepare_data(df:pd.DataFrame):
    # 使用 to_datetime() 将时间列转化为 datetime
    df['time']=pd.to_datetime(df['report_time'])
    
    #删除旧列
    df = df.drop(columns=['report_time'])
    
    # 将 time 设为df的索引
    df=df.set_index('time')
    
    # 排序
    df=df.sort_values('time')
    
    # 缺失值前向填充
    df[['mem_usage','disk_usage','cpu_usage']]=df[['mem_usage','disk_usage','cpu_usage']].ffill()
    
    return df