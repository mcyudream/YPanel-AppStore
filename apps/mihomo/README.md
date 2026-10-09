# Mihomo（Clash Meta）+ metacubexd 面板

Mihomo（Clash Meta 内核）代理核心 + metacubexd 官方可视化管理面板，一个应用带齐：混合代理端口（HTTP/SOCKS5）、规则/规则集、TUN、可视化节点与连接管理。安装即启动，默认全直连，导入你的节点/订阅后即用。

## 面板使用

1. 浏览器访问 `http://<主机IP>:<面板访问端口>` 打开 metacubexd。
2. 后端地址填 `http://<主机IP>:<外部控制器端口>`，密钥默认为空，点 Add 切换即可管理。
3. 节点/订阅：面板「配置」页可直接编辑 config.yaml，或经面板文件管理改应用目录 `data/mihomo/config.yaml`，改完重启容器生效。

## 代理地址

- 局域网设备：`http://<主机IP>:<代理端口>`（HTTP 与 SOCKS5 同端口混合）
- 同一容器网络内的其他容器：`http://<应用名>:7890`（如 `http://mihomo:7890`）

## 常用调整

- **订阅**：把 `data/mihomo/config.yaml` 的 `proxies: []` 换成节点列表，或启用注释里的 `proxy-providers` 订阅拉取（默认每日自动更新）。
- **控制器密钥**：默认留空仅建议内网使用；公网暴露前在 config.yaml 设 `secret` 并重启。
- **TUN 模式**：默认关闭（无需特权）。需要时在 config.yaml 开 `tun`，并在应用的参数编辑（.env）之外给 mihomo 容器加 `NET_ADMIN` 能力与 `/dev/net/tun` 挂载（高级用法）。
- **镜像拉取**：面板镜像来自 ghcr.io，节点拉不动时在「Docker 配置」里配好加速器/镜像源后重装即可。

## 数据

配置与运行数据在应用目录 `data/mihomo/`（含 config.yaml 与缓存），重装应用保留。
