import pandas as pd

# 3-sigma 动态阈值异常检测
class ThreeSigmaDetector:
    def __init__(self,df,column) -> None:
        if isinstance(df,pd.DataFrame):
            self.data=df[column]
        else:
            self.data=df
        self.column=column
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
        return self
    
    # 返回一个布尔 Series,每个点是否为异常(True = 异常)   
    def detect(self):
        return (self.data>self.upper) | (self.data<self.lower)
    
    # 返回只包含异常点的 DataFrame
    def get_anomalies(self):
        return self.data[self.detect()]
    
    # 打印: 总点数、异常点数、异常率、上下界
    def summary(self):
        abnormity=self.detect()
        print(f"总点数: {len(self.data)}")
        print(f"均值: {self.mean:.4f}, 标准差: {self.std:.4f}")
        print(f"正常范围: [{self.lower:.4f}, {self.upper:.4f}]")
        print(f"异常点数: {abnormity.sum()} ({abnormity.mean()*100:.2f}%)")