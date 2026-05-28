# 🎯 SRE + AIOps 个人学习路线图

> 基于你当前的 SRE-STUDY 项目现状定制 | 生成日期: 2026-05-16

---

## 📊 当前能力定位

```
已覆盖: 清单第 1-18, 26-41, 44-45, 51-52 项 (约 35/140)
位置:   第二阶段中期 → 正过渡到第三阶段（监控与可观测性）
```

你已有一个**可运行的 Python SRE 监控引擎**（`main_sre_engine.py` + `sre_monitor_hub.py`），
下一步的关键是：**从"自己写监控"升级到"使用工业标准工具链"，并逐步引入 AIOps 智能分析能力。**

---

## 🗺️ 总体学习路线（4 个阶段，12 周）

```
Week 1-2  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  补齐基础 + Prometheus/Grafana 入门
Week 3-4  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  Kubernetes 实战部署
Week 5-6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  日志体系 + 链路追踪
Week 7-8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  SLO/SLI + 告警体系
Week 9-10 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  AIOps 算法实战
Week 11-12▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  SRE 文化 + 综合项目
```

---

## 📅 第 1-2 周：补齐基础 + Prometheus/Grafana 入门

### 🎯 目标
- 补齐清单中跳过的项目
- 将你的监控系统接入 Prometheus + Grafana

### 📚 理论清单（对应清单项）
| # | 内容 | 说明 |
|---|------|------|
| 7 | TCP/UDP 原理 | 你监控 SSH 连接，理解 TCP 三次握手更能定位问题 |
| 8 | HTTP/HTTPS 协议 | 后续所有工具（Prometheus/Grafana/K8s API）都基于 HTTP |
| 9 | DNS 解析 | 容器间通信依赖 DNS，dig 排查必备 |
| 21 | Go 并发原语 | 大部分云原生工具是 Go 写的，了解 goroutine/channel |
| 23 | Git 分支与冲突 | 你的项目用 Git，补充分支协作技能 |
| 28 | 正则表达式 | 你的 `ip.py` 已用正则，系统学习后会更高效 |
| 51-55 | Prometheus + Grafana 全链路 | 工业标准监控体系 |

### 🛠️ 动手实践（在你的工作区中）

#### 任务 1: 为你的 Python 项目添加 Prometheus 指标暴露
```bash
# 在你的 .venv 中安装 prometheus_client
pip install prometheus-client
```

创建 `utils/metrics.py`，暴露你的监控数据为 Prometheus 格式：
- 将 `get_memory_info()`, `get_disk_usage_report()`, `get_cpu_usage()` 转为 Prometheus Gauge
- 启动一个 HTTP 服务（端口 8000）暴露 `/metrics` 端点

#### 任务 2: 搭建 Prometheus + Grafana
在 `docker-compose.yml` 中添加 Prometheus 和 Grafana 服务，让它们采集你的 Python 应用指标。

#### 任务 3: 创建 Grafana 仪表板
- 导入 Node Exporter 仪表板（ID: 1860）
- 自建一个 SRE 综合面板，展示你的四维指标

### ✅ 第一周检查点
- [ ] Prometheus 能抓取到你的 Python 应用的 `/metrics`
- [ ] Grafana 中能看到 CPU/内存/磁盘的时间序列图
- [ ] 能用 PromQL 写出 `rate()`, `avg_over_time()`, `increase()` 查询

---

## 📅 第 3-4 周：Kubernetes 实战部署

### 🎯 目标
将你的 SRE 监控系统容器化部署到 K8s 集群

### 📚 理论清单
| # | 内容 |
|---|------|
| 42-50 | K8s 全系列（Pod/Deployment/Service/Ingress/ConfigMap/Secret/PVC） |
| 61 | 健康检查探针（liveness/readiness/startup） |

### 🛠️ 动手实践

#### 任务 1: 本地搭建 K3s 或 Minikube
```bash
# 安装 Minikube（轻量 K8s）
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube start
```

#### 任务 2: 编写 K8s 部署清单
为你的项目创建以下 YAML 文件（放在 `k8s/` 目录）：
```
k8s/
├── namespace.yaml        # sre-staging 命名空间
├── mysql-deployment.yaml # MySQL StatefulSet + Service
├── mysql-secret.yaml     # 数据库密码（Secret）
├── sre-app-deployment.yaml # 你的监控引擎 Deployment
├── sre-app-configmap.yaml  # 配置（ConfigMap）
└── prometheus-grafana.yaml # 监控栈
```

#### 任务 3: 添加健康检查
在你的 Python 应用中暴露 `/health` 和 `/ready` 端点，配置 livenessProbe 和 readinessProbe。

### ✅ 第二周检查点
- [ ] K8s 集群中所有 Pod 状态为 Running
- [ ] `kubectl logs` 能查看你的监控引擎日志
- [ ] 健康检查探针正常工作

---

## 📅 第 5-6 周：日志体系 + 链路追踪

### 🎯 目标
从简单的 print/log 文件升级到结构化日志系统

### 📚 理论清单
| # | 内容 |
|---|------|
| 26 | Linux 日志体系（journald/rsyslog） |
| 56 | ELK/EFK 栈 |
| 57 | Loki + LogQL |
| 58 | OpenTelemetry + Jaeger |
| 69 | 日志结构化（你已经用正则做了！） |

### 🛠️ 动手实践

#### 任务 1: 改造你的日志系统
将 `utils/log.py` 升级为结构化日志（使用 Python `logging` 模块或 `structlog`）：
```python
# 输出 JSON 格式日志，包含 timestamp/level/component/message
{"timestamp":"2026-05-16T10:00:00","level":"WARNING","component":"security","message":"High SSH failure: 15 attempts from 192.168.1.100"}
```

#### 任务 2: 搭建 Loki + Promtail
在 `docker-compose.yml` 中添加 Loki 和 Promtail，将你的结构化日志发送到 Loki，并在 Grafana 中关联查询。

#### 任务 3: 理解分布式追踪
- 阅读 OpenTelemetry 官方文档
- 手动创建一个 Trace（包含多个 Span），理解 TraceID/SpanID 的传递

---

## 📅 第 7-8 周：SLO/SLI + 告警体系

### 🎯 目标
从"凭感觉设阈值"升级到"基于 SLO 的科学告警"

### 📚 理论清单
| # | 内容 |
|---|------|
| 59-60 | Alertmanager + On-Call 值班体系 |
| 62-64 | SLI/SLO/错误预算 |
| 76-79 | API 网关 / 熔断 / 限流 / 降级 |

### 🛠️ 动手实践

#### 任务 1: 为你的系统定义 SLI
```
SLI-1: CPU 使用率 < 85%（时间窗口: 5 分钟）
SLI-2: 内存使用率 < 90%
SLI-3: 磁盘使用率 < 90%
SLI-4: SSH 爆破检测响应 < 30 秒
```

#### 任务 2: 定义 SLO 和错误预算
```
SLO: 99.9% 的 5 分钟窗口内，CPU < 85%
错误预算: 每月允许 43 分钟的不达标时间
```

#### 任务 3: 配置 Prometheus 告警规则 + Alertmanager
- 创建告警规则文件（`.yml`），基于 SLO 燃烧率触发告警
- 配置 Alertmanager 的告警分组和路由

---

## 📅 第 9-10 周：AIOps 算法实战

### 🎯 目标
在你已有的监控数据上跑 AIOps 算法，从"阈值告警"升级到"智能异常检测"

### 📚 理论清单
| # | 内容 |
|---|------|
| 65-67 | AIOps 五大场景 + 数据预处理 |
| 71-73 | 数学基础 + pandas/numpy + 特征工程 |
| 86-91 | 异常检测算法全系列 |
| 92-94 | 日志异常检测 |
| 97-98 | 根因定位（相关性/因果推断） |

### 🛠️ 动手实践（基于你的 MySQL 监控数据）

#### 任务 1: 从数据库提取训练数据
```python
# 从 monitor_log 表读取历史 CPU/内存数据
# 用 pandas 做数据清洗和可视化
```

创建 `aiops/data_loader.py` — 从你的 MySQL `monitor_log` 表中提取时序数据。

#### 任务 2: 实现 3-Sigma 动态阈值
创建 `aiops/anomaly_detector.py`：
- 3-Sigma 异常检测
- IQR 箱线图异常检测
- 与你现有的固定阈值（93%）对比效果

#### 任务 3: 实现孤立森林（Isolation Forest）
用 sklearn 的 IsolationForest 检测多维异常：
- 输入：CPU + 内存 + 磁盘 + 登录失败次数
- 输出：异常分数 + 是否异常

#### 任务 4: 智能告警降噪
创建 `aiops/alert_dedup.py`：
- 滑动窗口聚合（30 秒内的同类告警合并）
- 依赖关系屏蔽（磁盘满导致的所有下游告警归并为一个）

---

## 📅 第 11-12 周：SRE 文化 + 综合项目

### 🎯 目标
完成综合项目 + 理解 SRE 方法论

### 📚 理论清单
| # | 内容 |
|---|------|
| 105-108 | 事件管理 / 无指责复盘 / Toil 自动化 |
| 111-112 | 压测 + 成本优化 |
| 128-131 | 技术写作 / 沟通 / 持续学习 |

### 🛠️ 综合项目：SRE 智能运维平台 v2.0

将前面所有学到的内容整合成一个完整平台：

```
SRE-STUDY/
├── k8s/                    # K8s 部署清单
├── aiops/                  # AIOps 算法模块
│   ├── data_loader.py      # 数据加载
│   ├── anomaly_detector.py # 异常检测
│   └── alert_dedup.py      # 告警降噪
├── monitoring/             # 监控配置
│   ├── prometheus.yml      # Prometheus 配置
│   ├── alert_rules.yml     # 告警规则
│   └── dashboards/         # Grafana 仪表板 JSON
├── docker-compose.yml      # 完整技术栈
│   ├── mysql
│   ├── sre_engine
│   ├── prometheus
│   ├── grafana
│   ├── loki
│   └── alertmanager
└── docs/                   # 文档
    ├── SLI_SLO.md          # SLO 定义
    ├── runbook.md          # 运维手册
    └── postmortem_template.md # 复盘模板
```

### ✅ 最终检查点
- [ ] 完整的 Prometheus + Grafana + Loki + Alertmanager 监控栈运行中
- [ ] AIOps 异常检测模块正常工作，能比固定阈值更早发现问题
- [ ] 告警降噪有效（告警数量减少 60%+）
- [ ] SLO 文档和运维手册就绪

---

## 📋 每周学习节奏建议

```
周一-周二：理论学习（阅读文档 + 看视频）
周三-周四：动手编码（在你的 SRE-STUDY 项目中实现）
周五：     复习 + 写笔记 + 打勾清单
周末：     回顾本周内容，准备下周
```

---

## 📊 140 项清单覆盖进度追踪

| 阶段 | 总项数 | 已完成 | 进行中 | 待开始 |
|------|--------|--------|--------|--------|
| 一、基础核心 | 25 | ~20 | 5 | 0 |
| 二、运维自动化 | 25 | ~12 | 8 | 5 |
| 三、监控可观测 | 14 | ~3 | 5 | 6 |
| 四、AIOps 基础 | 9 | 0 | 0 | 9 |
| 五、分布式系统 | 12 | 0 | 0 | 12 |
| 六、AIOps 算法 | 19 | 0 | 0 | 19 |
| 七、SRE 流程 | 8 | 0 | 0 | 8 |
| 八、AIOps 工程化 | 6 | 0 | 0 | 6 |
| 九、进阶云原生 | 9 | 0 | 0 | 9 |
| 十、软技能 | 4 | 0 | 0 | 4 |

---

## 🚀 立即开始的第一步

> **现在就可以做的事情：安装 Prometheus Client，给你的 Python 应用加 `/metrics` 端点！**

```bash
# 在当前终端执行
source /home/liliana0521/SRE-STUDY/.venv/bin/activate
pip install prometheus-client
```

我已经帮你规划好了，你想从哪个阶段开始？建议按顺序从**第 1 周的任务 1**开始，我可以直接辅助你写代码！
