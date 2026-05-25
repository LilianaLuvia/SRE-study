from dotenv import load_dotenv
load_dotenv()
from aiops.anomaly_detector import ThreeSigmaDetector, IQRDetector, IsolationForestDetector
from utils.getTime import now
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# 随机产生n个异常点(时间和值随机)
def generate_anomalies(base_df:pd.DataFrame,n:int=10,column=None,seed=42):
    if column==None:
        column=['cpu_usage', 'mem_usage', 'disk_usage']
    
    np.random.seed(seed)
    anomalies=[]
    
    # 获取时间序列
    time_range=base_df.index
    n_times = len(time_range)
    
    # 创建异常点
    for _ in range(n):
        t_min = time_range.min()
        t_max = time_range.max()
        total_seconds = (t_max - t_min).total_seconds()
        random_seconds = np.random.uniform(0, total_seconds)
        random_time = t_min + pd.Timedelta(seconds=random_seconds)
        row={'time':random_time}
        for col in column:
            mean_val=base_df[col].mean()
            std_val=base_df[col].std()
            
            # 计算异常值
            abnormal_val = mean_val + np.random.uniform(1.5, 2.5) * std_val
            row[col]=abnormal_val
            
        anomalies.append(row)
        
    anomalies_df=pd.DataFrame(anomalies)
    
    # 设置time为索引
    anomalies_df=anomalies_df.set_index('time')
    
    return anomalies_df

# 注入异常
def inject_anomalies(main_df:pd.DataFrame,anomalies_df:pd.DataFrame):
    combined_df=pd.concat([main_df,anomalies_df])
    combined_df=combined_df.sort_index()
    return combined_df

# 运行三种异常检测算法
def detect_all(combined_df:pd.DataFrame,column:str):
    anomoalies_df={}
    
    df_3sigma=ThreeSigmaDetector(combined_df,column)
    df_3sigma.fit()
    combined_df[f'{column}_3sigma']=df_3sigma.detect()
    
    df_iqr=IQRDetector(combined_df,column)
    df_iqr.fit()
    combined_df[f'{column}_iqr']=df_iqr.detect()
    
    df_iforest=IsolationForestDetector(combined_df)
    df_iforest.fit()
    combined_df[f'{column}_iforest']=df_iforest.detect()
    
    return combined_df

# 绘制三种算法对比图
def plot_comparison(df:pd.DataFrame,save_path=None):
    if save_path==None:
        save_path=os.path.join(os.getcwd(),'logs','anomaly_report.png')
    
    # 对三种指标进行异常检测
    for col in ['cpu_usage','mem_usage','disk_usage']:
        df=detect_all(df,col)
    
    fig,axes=plt.subplots(3,1,figsize=(14,10),sharex=True)
    
    # 三个指标
    metrics=[(axes[0],'cpu_usage','cpu'),(axes[1],'mem_usage','mem'),(axes[2],'disk_usage','disk')]
    
    colors={'3sigma':'red','iqr':'orange','iforest':'purple'}
    marker={'3sigma':'x','iqr':'^','iforest':'*'}
    
    for axe,col,label in metrics:
        axe.plot(df.index,df[col],color='steelblue', alpha=0.6, label=label)
        
        for algo,color in colors.items():
            anomaly_algo=f"{col}_{algo}"
            anomalies=df[df[anomaly_algo]]
            axe.scatter(anomalies.index,anomalies[col],color=color,marker=marker[algo],s=80,label=f"{algo}")
            
        axe.set_ylabel(col)
        axe.set_title(col.upper())
        axe.legend(loc="upper right",fontsize=8)

    axes[2].set_xlabel('Time')
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path),exist_ok=True)
        plt.savefig(save_path)
    plt.show()

# 输出异常检测报告
def generate_markdown_report(df:pd.DataFrame,img_path=None):
    if img_path==None:
        img_path=os.path.join(os.getcwd(),'logs','anomaly_report.md')
    
    df_3sigma=ThreeSigmaDetector(df,"cpu_usage")
    df_3sigma.fit()
    res_3sigma = df_3sigma.abnormity
    df_iqr=IQRDetector(df,"cpu_usage")
    df_iqr.fit()
    res_iqr=df_iqr.abnormity
    df_iforest=IsolationForestDetector(df)
    df_iforest.fit()
    res_iforest = df_iforest.anomalies
    
    report=f"""
# SRE 异常检测报告
> 生成时间: {now()}

## 数据概况
- 总点数: {len(df)}
- 时间范围: {df.index.min()} ~ {df.index.max()}

## 三种算法对比(异常率仅统计CPU)
| 算法 | 异常数 | 异常率 |
|------|--------|--------|
| 3-Sigma | {res_3sigma.sum()} | {res_3sigma.mean()*100:.2f}% |
| IQR | {res_iqr.sum()} | {res_iqr.mean()*100:.2f}% |
| Isolation Forest | {res_iforest} | {(res_iforest/len(df))*100:.2f}% |
## 可视化
![异常检测对比](anomaly_report.png)"""

    if img_path:
        os.makedirs(os.path.dirname(img_path),exist_ok=True)
        with open(img_path,'w',encoding='utf-8') as f:
            f.write(report)

if __name__ == '__main__':
    from aiops.data_loader import load_from_db, prepare_data
    
    # 1. 加载真实数据
    df = load_from_db(limit=1000)
    df = prepare_data(df)
    
    # 2. 生成异常并注入（随机分散在整个时间范围）
    anom = generate_anomalies(df, n=15)
    df = inject_anomalies(df, anom)
    
    # 3. 画图 + 报告
    plot_comparison(df)
    generate_markdown_report(df)
    print("异常时间戳:", anom.index.tolist())