# SRE-STUDY 系统安全与性能审计自动化
## 项目简介
  本项目暂时主要基于Python3 开发的SRE自动化监控方案。目前主要实现了底层日志流实时监听、内存和磁盘指标采集、安全风险自动化分析。
  目前项目状态:【Developping】

## 核心架构
  该项目主要采用事件驱动 (Event-Driven) 与 流式处理 (Streaming)，主要包含以下核心功能: 
1. 实时日志审计
    * 流式监听: 模拟```tail -f```,控制文件指针偏移，实现对日志的增量读取
    * 正则结构化: 利用正则表达式命名组 (?P\<name>) ,将SSH登录日志解析为结构化数据

2. 多维指标监控
    * 内存画像: 实时采集系统可用内存、使用率及状态
    * 磁盘审计: 支持指定挂载点的空间分析，包括总量、已用、剩余及百分比监控。
    * 硬件预警: 内置阈值判定逻辑，自动识别 HEALTHY、WARNING 或 DANGER 状态。

3. 安全分析引擎
    * 攻击画像: 利用 collections.Counter 实时更新高频登录错误 IP 账本
    * 风险评估: 内置智能评估逻辑，根据频率自动判定风险等级（NORMAL / WARNING / CRITICAL）
    * 防抖机制: 实现时间窗口控制，防止在高频事件触发下造成的系统 IO 过载

4. 自动化报告
    * 动态报表: 可自动生成 Markdown 格式的系统审计报告
    * 可视化渲染: 将复杂数据转化为 ASCII 柱状图及状态指示器

## 项目结构(暂时最主要的模块)
```
.
└── SRE-STUDY
    ├── utils
    │   ├── alert_utils.py
    │   ├── disk_utils.py
    │   ├── ip_utils.py
    │   ├── json_utils.py
    │   ├── log_utils.py
    │   ├── memory_utils.py
    │   ├── process_utils.py
    │   └── sys_utils.py
    ├── sre_live_tailer.py
    ├── sre_cron_manager.py
    ├── sre_monitor_pro.py
    ├── sre_report_generator.py
    ├── sre_monitor_hub.py
    └── main_sre_engine.py
```

---
本项目遵循常规提交规范 (Conventional Commits)，确保工程化开发的可追溯性