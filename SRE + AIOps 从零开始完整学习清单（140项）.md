# SRE + AIOps 从零开始完整学习清单（140项）

## 第一阶段：基础核心（Linux/网络/编程）

- [ ] 1. Linux命令行：文件操作（ls, cd, cp, mv, rm, mkdir, touch, cat, less, head, tail）
- [ ] 2. Linux文本处理：grep, awk, sed, cut, sort, uniq, wc
- [ ] 3. Vim/Nano 编辑器基础操作（编辑、保存、搜索、退出）
- [ ] 4. Shell脚本：变量、条件判断（if）、循环（for/while）、函数、退出码
- [ ] 5. 进程管理：ps, top/htop, kill, jobs, bg, fg, nice/renice
- [ ] 6. 文件权限与用户组：chmod, chown, useradd, usermod, su, sudo
- [ ] 7.  网络基础：OSI七层模型、TCP三次握手与四次挥手、UDP特点
- [ ] 8. HTTP/HTTPS协议：请求方法、常见状态码、请求头与响应头
- [ ] 9. DNS解析原理：A/AAAA/CNAME/TXT记录、dig/nslookup使用
- [ ] 10. 负载均衡基础概念：四层与七层区别、轮询/最少连接/IP哈希算法
- [ ] 11. 编程语言Python基础：安装、pip、虚拟环境（venv）
- [ ] 12. Python语法：变量、数据类型、列表/字典/元组/集合推导式
- [ ] 13. Python流程控制：if/elif/else、for/while循环、break/continue
- [ ] 14. Python函数：定义、参数类型、返回值、lambda表达式
- [ ] 15. Python面向对象：类与对象、继承、`__init__`方法、self
- [ ] 16. Python异常处理：try/except/finally、自定义异常
- [ ] 17. Python常用标准库：os、sys、subprocess、json、argparse
- [ ] 18. Python第三方库：requests、PyYAML、kubernetes客户端
- [ ] 19. 编程语言Go基础（进阶核心）：安装、Go Modules、基本语法
- [ ] 20. Go语言特点：包管理、defer、指针、结构体、interface
- [ ] 21. Go并发原语：goroutine、channel、select语句
- [ ] 22. 代码版本控制Git：初始化仓库、add/commit/log/diff
- [ ] 23. Git分支管理：创建/切换/合并分支、解决合并冲突
- [ ] 24. Git协作流程：clone、push、pull、fetch、rebase与merge区别
- [ ] 25. Git远程仓库：关联远程、拉取请求流程

## 第二阶段：运维与自动化（系统/容器/K8s）

- [ ] 26. 系统日志：Linux日志体系、journald查看、rsyslog配置远程日志
- [ ] 27. systemd服务管理：编写service单元文件、systemctl常用命令
- [ ] 28. 正则表达式基础：元字符、分组与捕获、贪婪与非贪婪
- [ ] 29. 定时任务：crontab格式与配置、systemd timer编写
- [ ] 30. SSH免密认证：生成密钥对、配置authorized_keys、ssh-agent使用
- [ ] 31. 跳板机/代理场景：SSH隧道、ProxyJump
- [ ] 32. 防火墙基础：iptables五链、常用规则编写
- [ ] 33. 存储管理：磁盘分区、文件系统创建、挂载
- [ ] 34. LVM逻辑卷管理：PV/VG/LV创建与扩展
- [ ] 35. 内存管理：free命令、swap分区/文件创建与优先级
- [ ] 36. 容器基础Docker：安装、镜像拉取与运行
- [ ] 37. Dockerfile编写：FROM、RUN、COPY/ADD、CMD/ENTRYPOINT
- [ ] 38. Docker镜像分层原理、构建优化（多阶段构建）
- [ ] 39. Docker网络模式：bridge、host、none、自定义桥接网络
- [ ] 40. Docker卷管理：bind mount、volume、tmpfs挂载
- [ ] 41. 容器资源限制：CPU、内存限制
- [ ] 42. 容器编排Kubernetes核心概念：集群、节点、Pod、控制平面组件
- [ ] 43. kubectl安装与配置：kubeconfig文件、上下文切换
- [ ] 44. kubectl常用命令：get/describe/create/apply/delete/logs/exec
- [ ] 45. Pod生命周期：pause容器、init容器、钩子
- [ ] 46. 控制器：Deployment、StatefulSet、DaemonSet
- [ ] 47. 服务发现：ClusterIP、NodePort、LoadBalancer类型的Service
- [ ] 48. Ingress：暴露HTTP/HTTPS路由、安装Ingress Controller
- [ ] 49. 配置管理：ConfigMap、Secret
- [ ] 50. 存储卷：emptyDir、hostPath、PersistentVolumeClaim（PVC）

## 第三阶段：监控与可观测性（Metrics/Logs/Tracing）

- [ ] 51. 指标系统Prometheus：架构、安装、配置文件
- [ ] 52. PromQL基础：瞬时向量/区间向量、标签匹配、常用函数
- [ ] 53. Prometheus指标类型：Counter、Gauge、Histogram、Summary
- [ ] 54. Exporters：node_exporter、kube-state-metrics
- [ ] 55. 可视化Grafana：数据源添加、仪表板创建与编辑
- [ ] 56. 日志系统：EFK/ELK栈（Elasticsearch/Logstash/Kibana）
- [ ] 57. 轻量级日志方案Loki：与Prometheus标签对齐、LogQL查询
- [ ] 58. 链路追踪：OpenTelemetry标准、Jaeger架构
- [ ] 59. 告警体系：Prometheus告警规则、Alertmanager配置
- [ ] 60. On-Call基础：告警分级、值班轮转、升级策略、应急预案
- [ ] 61. 健康检查：livenessProbe、readinessProbe、startupProbe
- [ ] 62. SLI定义：延迟、错误率、吞吐量、可用性
- [ ] 63. SLO定义：目标值、时间窗口、排除条件
- [ ] 64. 错误预算计算与消耗控制策略

## 第四阶段：AIOps基础（数据处理与异常检测前置）

- [ ] 65. AIOps核心概念：五大场景（异常检测、根因分析、故障预测、智能告警、自动修复）
- [ ] 66. 运维数据分类：时序指标、日志、链路追踪、事件
- [ ] 67. 数据预处理基础：缺失值填充、去重、归一化、时间戳对齐、采样降频
- [ ] 68. 时序数据库进阶：VictoriaMetrics/Thanos（长期存储与高基数压缩）
- [ ] 69. 日志结构化：JSON解析、键值对提取、模板化（grok/正则分组）
- [ ] 70. 关联分析基础：通过TraceID/RequestID/IP/时间窗口关联不同数据源
- [ ] 71. AI/ML数学基础：统计学（均值/方差/分位数）、线性代数（向量/矩阵）、微积分（梯度概念）
- [ ] 72. Python数据处理：pandas（Series/DataFrame）、numpy（数组运算）
- [ ] 73. 特征工程基础：滑动窗口、差分、归一化、类别编码

## 第五阶段：分布式系统与高可用设计

- [ ] 74. CAP定理：一致性、可用性、分区容错性的取舍
- [ ] 75. 服务发现机制：客户端发现、服务端发现、K8s内置CoreDNS
- [ ] 76. API网关：Kong/Traefik——认证、限流、路由
- [ ] 77. 熔断器：状态机（关闭→打开→半开）
- [ ] 78. 限流算法：漏桶、令牌桶、滑动窗口、分布式限流
- [ ] 79. 降级与重试：降级预案、重试策略、退避算法
- [ ] 80. 分布式追踪上下文：TraceID、SpanID跨服务传递
- [ ] 81. 混沌工程原则：爆炸半径控制、稳态假设
- [ ] 82. 容量规划：基于历史监控数据预测峰值
- [ ] 83. 水平扩展：无状态直接扩容、有状态分片
- [ ] 84. 数据库连接池：连接泄漏检测
- [ ] 85. 慢查询分析：MySQL慢日志、Elasticsearch慢查询

## 第六阶段：AIOps核心算法与实践

- [ ] 86. 异常检测——静态阈值：单指标固定上下限
- [ ] 87. 异常检测——动态阈值：3-Sigma、IQR箱线图
- [ ] 88. 异常检测——时间序列预测：移动平均、指数平滑（Holt-Winters）
- [ ] 89. 异常检测——Prophet模型：考虑周期性/节假日
- [ ] 90. 异常检测——无监督模型：孤立森林、DBSCAN
- [ ] 91. 异常检测——智能基线学习：自动识别波动规律、预测带
- [ ] 92. 日志异常检测——模板法：Drain算法自动提取日志模板
- [ ] 93. 日志异常检测——统计法：TF-IDF + 聚类
- [ ] 94. 日志异常检测——深度学习方法：Deeplog/Lolog（了解原理）
- [ ] 95. 智能告警降噪：告警聚合、依赖关系屏蔽
- [ ] 96. 告警收敛：基于滑动窗口的count-based与time-based
- [ ] 97. 根因定位——相关性分析：皮尔逊/斯皮尔曼相关系数
- [ ] 98. 根因定位——因果推断：Granger因果检验
- [ ] 99. 根因定位——调用链分析：故障传播路径跟踪
- [ ] 100. 根因定位——随机下探/二分法：微观定位变更版本
- [ ] 101. 异常预测（故障预兆）：资源耗尽线性延伸、季节性高峰期预警
- [ ] 102. 容量预测：ARIMA/SARIMA预测未来QPS/CPU
- [ ] 103. LLM在AIOps中的应用：提示词工程（日志总结根因）、RAG（结合知识库）
- [ ] 104. 模型评估：准确率/召回率/F1值、误报率/漏报率

## 第七阶段：SRE专有流程与稳定性文化

- [ ] 105. 事件管理：IM角色划分、响应SLA、协作流程
- [ ] 106. 无指责复盘文化：5 Whys根因分析
- [ ] 107. 运维琐事（Toil）定义与自动化
- [ ] 108. SRE与Dev团队协作模型：共享错误预算
- [ ] 109. 变更管理：变更分类、审批窗口、回滚预案
- [ ] 110. 风险评估：变更影响面、灰度范围
- [ ] 111. 性能压测工具：wrk、JMeter、Locust
- [ ] 112. 成本优化：资源利用率提升、预留实例、闲置回收

## 第八阶段：AIOps工程化与落地

- [ ] 113. AIOps工程平台选型：开源、商业、自研
- [ ] 114. 模型离线训练与在线推理管道：训练→存储→实时推理
- [ ] 115. 反馈闭环机制：人工确认回流→定期重训练
- [ ] 116. 异常处理自动化：检测触发自愈（重启/扩容/切流）
- [ ] 117. 模型可解释性：SHAP值（特征贡献度分析）
- [ ] 118. 实践经验陷阱：抖动敏感、节假日波动、冷启动问题

## 第九阶段：进阶云原生与扩展

- [ ] 119. 服务网格Istio：数据平面、控制平面、流量管理
- [ ] 120. eBPF基础：原理、常见项目（Cilium/Falco/Pixie）
- [ ] 121. 分布式数据库：TiDB/CockroachDB
- [ ] 122. 消息队列Kafka：架构、生产消费模型
- [ ] 123. RabbitMQ：AMQP模型、Exchange类型
- [ ] 124. 零信任安全模型：mTLS、微隔离
- [ ] 125. 公有云基础（至少一个）：AWS/阿里云/腾讯云
- [ ] 126. 云上K8s服务：EKS/ACK/TKE
- [ ] 127. 云成本分析与优化

## 第十阶段：软技能与持续成长

- [ ] 128. 技术文档写作：故障复盘报告、SLO文档、运维手册
- [ ] 129. 有效沟通：跨团队推动、数据支撑决策
- [ ] 130. 思维习惯：从修复到根除、从手动到代码
- [ ] 131. 持续学习渠道：SREcon、技术博客、社区