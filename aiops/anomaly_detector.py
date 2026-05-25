import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

# 3-sigma 动态阈值异常检测
class ThreeSigmaDetector:
    def __init__(self,df,column:str) -> None:
        if isinstance(df,pd.DataFrame):
            self.data=df[column]
        else:
            self.data=df
        self.column=column
        self.abnormity=None
        self.mean=None
        self.std=None
        self.upper=None
        self.lower=None
    
    # 计算均值、标准差、上界、下界   
    def fit(self):
        self.mean=self.data.mean()
        self.std=self.data.std()
        self.upper=self.mean+3*self.std
        self.lower=max(0,self.mean-3*self.std)
        self.abnormity=self.detect()
        return self
    
    # 返回一个布尔 Series,每个点是否为异常(True = 异常)   
    def detect(self):
        return (self.data>self.upper) | (self.data<self.lower)
    
    # 返回只包含异常点的 DataFrame
    def get_anomalies(self):
        return self.data[self.detect()]
    
    # 打印: 总点数、异常点数、异常率、上下界
    def summary(self):
        self.abnormity=self.detect()
        print(f"总点数: {len(self.data)}")
        print(f"均值: {self.mean:.4f}, 标准差: {self.std:.4f}")
        print(f"正常范围: [{self.lower:.4f}, {self.upper:.4f}]")
        print(f"异常点数: {self.abnormity.sum()} ({self.abnormity.mean()*100:.2f}%)")
        
# IQR箱线图
class IQRDetector:
    def __init__(self,df,column,k:float=1.5) -> None:
        if isinstance(df,pd.DataFrame):
            self.data=df[column]
        else:
            self.data=df
        self.column=column
        self.k=k
        self.abnormity=None
        self.q1=None
        self.q3=None
        self.iqr=None
        self.upper=None
        self.lower=None
    
    # 计算均值、标准差、上界、下界   
    def fit(self):
        self.q1=np.percentile(self.data,25)
        self.q3=np.percentile(self.data,75)
        self.iqr=self.q3-self.q1
        self.upper=self.q3+self.k*self.iqr
        self.lower=max(0,self.q1-self.k*self.iqr)
        self.abnormity=self.detect()
        return self
    
    # 返回一个布尔 Series,每个点是否为异常(True = 异常)   
    def detect(self):
        return (self.data>self.upper) | (self.data<self.lower)
    
    # 返回只包含异常点的 DataFrame
    def get_anomalies(self):
        return self.data[self.detect()]
    
    # 打印: 总点数、异常点数、异常率、上下界
    def summary(self):
        self.abnormity=self.detect()
        print(f"总点数: {len(self.data)}")
        print(f"下界: {self.q1:.4f}, 上界: {self.q3:.4f}")
        print(f"正常范围: [{self.lower:.4f}, {self.upper:.4f}]")
        print(f"异常点数: {self.abnormity.sum()} ({self.abnormity.mean()*100:.2f}%)")

# 孤立森林(Isolation Forest)
class IsolationForestDetector:
    def __init__(self, df, columns=['cpu_usage', 'mem_usage', 'disk_usage'],contamination=0.05):
        self.data = df[columns]
        self.columns = columns
        self.contamination = contamination
        self.anomalies=None
        self.model=None
        self.labels=None
        self.scores=None
    
    def fit(self):
        self.model = IsolationForest(
            contamination=self.contamination,
            random_state=42
        )
        self.labels = self.model.fit_predict(self.data)
        # 转换为分数
        self.scores = self.model.decision_function(self.data)
        self.anomalies = (self.labels == -1).sum()
        return self
    
    def detect(self):
        return self.labels==-1
    
    def get_anomalies(self):
        return self.data[self.labels == -1]
    
    def summary(self):
        self.anomalies = (self.labels == -1).sum()
        print(f"总点数: {len(self.data)}")
        print(f"异常点数: {self.anomalies} ({self.anomalies/len(self.data)*100:.2f}%)")
        print(f"异常分数范围: [{self.scores.min():.4f}, {self.scores.max():.4f}]") # type:ignore