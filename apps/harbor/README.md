# Harbor — 云原生容器镜像仓库

CNCF 毕业项目，企业级 Docker/OCI 镜像仓库：漏洞扫描（Trivy）、镜像签名与内容信任、多租户 RBAC、跨仓库复制、垃圾回收与审计。本包按官方 v2.15.4 compose 结构适配（prepare 初始化 + 全组件）。

## 安装参数说明

| 参数 | 说明 |
|---|---|
| 访问主机名 | 必填。用户 `docker login` 使用的地址（公网 IP 或域名），**不要填 localhost / 127.0.0.1**；生成的访问地址为 `http://<主机名>:<端口>` |
| admin 初始密码 | 仅首次安装生效（之后在 Harbor UI 修改）；请避免 `$`、引号、反引号等特殊字符 |
| 数据库密码 | 内置 PostgreSQL 密码（随机默认即可） |
| HTTP 端口 | 面板映射端口，默认 30080 |

## 使用

- 浏览器访问 `http://<主机名>:<端口>`，用户名 `admin`，密码为安装时设置的 admin 初始密码。
- 登录仓库：`docker login <主机名>:<端口> -u admin`；HTTP 明文仓库，客户端需在 `daemon.json` 的 `insecure-registries` 中加入 `<主机名>:<端口>`（面板本机已自动放行同网段场景一般无需配置）。
- 一键反代：如需用域名反代 Harbor，主机名填该域名、端口填 80（或反代后端端口），保证 `http://<域名>` 与生成的访问地址一致，否则登录/推送会因 token 地址不匹配失败。

## 组件与数据

- 容器约 10 个（log/registry/registryctl/postgresql/redis/trivy/core/portal/jobservice/nginx + 一次性 prepare），内存占用约 1.5~2GB，镜像体积约 2GB。
- 数据全部持久化在项目目录 `./data/harbor/`（数据库、镜像存储、密钥、扫描缓存）；重装应用该目录保留。
- 组件日志走集中 syslog，落盘在宿主机 `/var/log/harbor/`（官方行为），`docker compose logs` 内容较少属正常。
- 升级版本：直接改版本重装，harbor-db 启动时自动执行数据库迁移；升级前建议先备份 `data/harbor/database` 目录。
