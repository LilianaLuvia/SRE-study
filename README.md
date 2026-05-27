# SRE-STUDY — 从零开始的 SRE + AIOps 实战平台

> 一个从零搭建的 SRE 学习项目，涵盖监控采集、可视化、告警体系、容器化部署、Kubernetes 编排全链路。
>
> 状态：**全部 5 阶段完成 ✅** | 持续迭代中

---

## 🏗️ 架构总览

```
                        ┌─────────────────────────────────────┐
                        │           Kubernetes (Minikube)      │
                        │  ┌──────────┐  ┌──────────────────┐ │
                        │  │  MySQL   │  │   sre-engine     │ │
                        │  │ Stateful │◀─│   Deployment     │ │
                        │  │   Set    │  │   (CPU/Mem/Disk  │ │
                        │  │  :3306   │  │    SSH 监控)     │ │
                        │  └──────────┘  └────────┬─────────┘ │
                        │                         │ :8000     │
                        └─────────────────────────┼───────────┘
                                                  │
    ┌─────────────────────────────────────────────┼───────────┐
    │                Docker Compose (开发环境)      │           │
    │  ┌──────────┐ ┌──────────┐ ┌──────────────┐ │           │
    │  │Alertmgmt │ │Prometheus│ │  sre_app     │◀┤           │
    │  │  :9093   │◀│  :9090   │◀│  :8000       │ │           │
    │  └──────────┘ └────┬─────┘ └──────────────┘ │           │
    │                    │                         │           │
    │  ┌─────────────────▼──┐   ┌──────────────┐  │           │
    │  │     Grafana        │   │    MySQL      │  │           │
    │  │     :3000          │   │    :3307      │  │           │
    │  └────────────────────┘   └──────────────┘  │           │
    └─────────────────────────────────────────────┘           │
```

---

## 🚀 快速启动

### 方式一：Docker Compose（开发/演示）

```bash
cp .env.example .env          # 编辑 .env 填入密码
docker compose up -d          # 启动全部 6 个服务
curl localhost:8000/metrics   # 验证指标端点
```

| 服务 | 地址 | 用途 |
|------|------|------|
| sre_app | `http://localhost:8000/metrics` | 指标暴露 |
| Prometheus | `http://localhost:9090` | 指标采集 + 告警规则 |
| Grafana | `http://localhost:3000` | 可视化仪表板 |
| Alertmanager | `http://localhost:9093` | 告警管理 |
| MySQL | `localhost:3307` | 历史数据持久化 |

### 方式二：Kubernetes（生产级部署）

```bash
minikube start --driver=docker
eval $(minikube docker-env)
docker build -t sre-engine:latest .
kubectl apply -f k8s/
kubectl port-forward -n sre-staging svc/sre-engine 8000:8000
```

---

## 📊 采集指标

| 指标名 | 类型 | 说明 |
|--------|------|------|
| `cpu_usage` | Gauge | CPU 使用率 % |
| `memory_usage` | Gauge | 内存使用率 % |
| `disk_usage` | Gauge | 磁盘使用率 % |
| `ssh_active_sessions` | Gauge | SSH 活跃连接数 |
| `ssh_failed_login_count` | Gauge | 登录失败总次数 |

---

## 🔔 告警规则

| 告警 | 条件 | 严重度 |
|------|------|--------|
| HighCPUUsage | `avg_over_time(cpu_usage[2m]) > 85` | warning |
| CriticalCPUUsage | `avg_over_time(cpu_usage[1m]) > 95` | critical |
| HighDiskUsage | `avg_over_time(disk_usage[2m]) > 90` | warning |
| SSHBruteForce | `ssh_failed_login_count > 20` | critical |

所有规则定义在 [`alert_rules.yml`](alert_rules.yml)，支持双层防抖（`avg_over_time` + `for` 持续时间）。

---

## 📁 项目结构

```
SRE-STUDY/
├── main_sre_engine.py          # 主巡检总线
├── sre_monitor_hub.py          # 数据聚合中心
├── utils/                      # 功能模块
│   ├── process.py              # CPU / 进程采集
│   ├── memory.py               # 内存采集
│   ├── disk.py                 # 磁盘采集
│   ├── ip.py                   # SSH 日志解析 + 安全量化
│   ├── alert.py                # 风险判定引擎
│   ├── database.py             # MySQL 持久化
│   ├── metrics.py              # Prometheus 指标暴露
│   ├── remedy.py               # 修复建议生成
│   ├── log.py                  # 日志管理
│   ├── json.py                 # 历史数据 JSON 存储
│   ├── system.py               # 系统信息解析
│   └── getTime.py              # 时间工具
├── aiops/                      # AIOps 智能分析模块
│   ├── data_loader.py          # 数据加载与预处理
│   ├── anomaly_detector.py     # 3 种异常检测算法
│   │   ├── ThreeSigmaDetector  #   3-Sigma 动态阈值
│   │   ├── IQRDetector         #   IQR 箱线图（抗极端值）
│   │   └── IsolationForestDetector  # 孤立森林（多维）
│   └── report.py               # 异常检测对比报告生成
├── k8s/                        # Kubernetes 部署清单
│   ├── namespace.yml           # sre-staging 命名空间
│   ├── mysql.yml               # MySQL StatefulSet + Service
│   ├── mysql-secret.yml        # 数据库密码 Secret
│   ├── sre-app.yml             # 引擎 Deployment + Service
│   └── sre-app-configmap.yml   # 非敏感配置
├── docx/                       # SRE 方法论文档
│   ├── SLI_SLO.md              # SLI / SLO / 错误预算定义
│   ├── postmotem_template.md   # 无指责故障复盘模板
│   └── Toil.md                 # Toil 识别与自动化计划
├── prometheus.yml              # Prometheus 抓取配置
├── alert_rules.yml             # Prometheus 告警规则
├── docker-compose.yml          # 本地开发栈（6 服务）
├── Dockerfile                  # 应用镜像
├── requirements.txt            # Python 依赖
├── STUDY_PLAN.md               # 12 周学习路线图
├── LICENSE                     # MIT License
└── archive/                    # 历史版本代码
```

---

## 🛠️ 技术栈

| 层 | 技术 |
|----|------|
| 语言 | Python 3.13 |
| 监控 | Prometheus + Grafana |
| 告警 | Alertmanager |
| AIOps | 3-Sigma / IQR / Isolation Forest |
| 数据处理 | pandas / numpy / matplotlib |
| 机器学习 | scikit-learn |
| 数据库 | MySQL 8.4 |
| 容器化 | Docker + Docker Compose |
| 编排 | Kubernetes (Minikube) |

---

## 🎯 学习路线

本项目遵循 [SRE + AIOps 从零开始完整学习清单](./SRE%20%2B%20AIOps%20从零开始完整学习清单（140项）.md)，详见 [STUDY_PLAN.md](./STUDY_PLAN.md)。

- [x] **阶段 1**：Linux / Python / 网络基础
- [x] **阶段 2**：Prometheus + Grafana + Alertmanager 监控体系
- [x] **阶段 3**：Docker Compose → Kubernetes 部署迁移
- [x] **阶段 4**：AIOps 算法（3-Sigma / IQR / Isolation Forest）
- [x] **阶段 5**：SRE 文化（SLI/SLO / 无指责复盘 / Toil 自动化）

---

## 📜 License

MIT — 学习自由，代码自由。