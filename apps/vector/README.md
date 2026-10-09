# Vector 日志采集器（容器日志 → 集中存储）

读取本机 Docker 守护进程的**全部容器日志**（含后续新启动的容器，自动跟随），按批量推送至集中存储 VictoriaLogs。

## 工作前提

- 同节点（或同网络）已通过应用商店安装 **VictoriaLogs**；
- 下方「VictoriaLogs 地址」填 VictoriaLogs 的可达地址：
  - 与本应用同网络（默认 `ypanel_default`）时填 `http://<victoria-logs容器名>:9428`（默认值即商店安装的容器名）；
  - 跨节点集中采集时填 `http://<VL所在机器内网IP>:<映射端口>`。

## 说明

- 需要 Docker Socket 只读挂载（`/var/run/docker.sock`），用于发现容器与读取日志流；
- 自动排除采集器自身容器的日志，避免回环；
- 日志字段映射：`message → _msg`、`timestamp → _time`，流字段为 `host,container_name,image`；
- 多节点部署：在每台节点上各安装一份本应用，指向同一个 VictoriaLogs 地址即可实现集中检索。
