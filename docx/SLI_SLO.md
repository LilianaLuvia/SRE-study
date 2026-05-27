# SRE-STUDY

## SLI-1:
- **指标**: `/metrics` 端点返回200的比例
- **测量方式**: Promethues `up{job="sre-engine"}`
- **SLO**: 99.9%
- **错误预算**: 每月允许43.2分钟不可用

## SLI-2:
- **指标**: `monitor_log` 表成功 INSERT 的比例
- **测量方式**: 应用日志中成功/失败计数
- **SLO**: 99.99%
- **错误预算**: 每月允许4.3分钟不可用

## SLI-3:
- **指标**: 异常告警抵达Alertmanager的时间
- **测量方式**: Prometheus `ALERTS` 的 `active_at` 减实际异常时间
- **SLO**: <30s