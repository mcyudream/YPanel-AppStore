# Element Skin — 现代化 Minecraft 皮肤站

面向高并发场景的现代化外置登录与材质平台：Go 后端 + Vue 3 前端 + PostgreSQL 18 + Redis 8，完整兼容 Yggdrasil（Authlib-Injector）协议，支持皮肤/披风上传、3D 预览、衣柜、公共皮肤库、OIDC/OAuth 第三方接入、Microsoft 正版角色绑定、多角色细粒度权限与通知中心。

## 面板使用

1. 浏览器访问 `http://<主机IP>:<端口>`（即安装时填写的「站点访问地址」）。
2. 首次启动后端自动生成 Yggdrasil 与 OIDC 密钥对（保存在应用目录 `data/app/`，请勿删除，删除后已签发材质全部失效）。
3. 启动器（Authlib-Injector）的 API 地址：`http://<主机IP>:<端口>/skinapi`（站点内也会展示）。

## 安装参数说明

| 参数 | 说明 |
|---|---|
| 站点访问地址 | 必填。浏览器实际访问地址（含端口），CORS / OIDC 回调 / 启动器都依赖它；换域名或端口后修改参数并重启生效 |
| JWT 密钥 / 身份加密密钥 / 数据库与 Redis 密码 | 安装向导自动随机生成；**身份加密密钥**用于加密 OIDC client secret 与外部 refresh token，配置过身份提供方之后不可更改 |

## 组件与数据

- 4 个容器：backend（站点+API）、webhook-worker（Webhook 投递，同镜像不暴露端口）、PostgreSQL 18、Redis 8；内存占用约 500MB。
- 数据全部持久化在应用目录 `data/`（数据库、密钥、材质文件、Redis 缓存），重装保留。
- 反代场景：整站反代到 `PANEL_APP_PORT` 即可，前后端同域（`/skinapi` 为 API 路径）；使用反代域名后记得把「站点访问地址」参数改成域名并重启。

## 升级注意

v4 的自动数据库升级只支持从 **v3.0.2+** 直接升级；更老版本必须先升到 v3.0.2。跨大版本升级前先备份 `data/` 目录（详见上游 Release Notes）。
