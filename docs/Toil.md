## Toil 识别与自动化计划

| Toil | 当前方式 | 自动化方案 |
|------|---------|-----------|
| 主机打开转发地址需手动重新转发端口 | 删除vscode中端口，重新添加 | kubectl port-forward 用 while true; do ...; done 包装成守护脚本，断线自动重连 |
