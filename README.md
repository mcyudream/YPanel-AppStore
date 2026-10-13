# YPanel AppStore — YPanel 官方应用源

[YPanel](https://github.com/mcyudream/ypanel)（YuDream 自研一体化服务器管理面板）的官方应用商店源，yp 格式，以 git 仓库分发（浅克隆 + 本地读包）。

## 三平台镜像（同步更新）

- GitHub：<https://github.com/mcyudream/YPanel-AppStore.git>
- Gitee：<https://gitee.com/mcyudream/YPanel-AppStore.git>（国内服务器推荐）
- GitLab：<https://gitlab.yudream.online/yudream/ypanel-appstore.git>（自建兜底源，内网服务器零外网依赖）

三边内容一致，面板接入时任选其一。

## 接入面板

面板「应用商店 → 源管理」→ 编辑内置「YPanel 官方源」→ URL 填上述仓库地址（类型 yp-git，分支 main）→ 保存后点「同步」。自定义源同样支持（新建 yp-git 类型源）。

## 目录结构

```
index.json                     # 源清单（唯一入口）
apps/<id>/logo.svg             # 图标（svg/png/jpg/webp）
apps/<id>/README.md            # 应用介绍（详情抽屉渲染 Markdown）
apps/<id>/<version>/package/   # 版本包目录（compose.yml + 附属文件，纯文本）
```

## index.json 字段

| 字段 | 说明 |
|---|---|
| `apps[].id` | 源内唯一 key（小写字母/数字/中划线） |
| `apps[].kind` | `app` 普通应用 / `service` 环境服务（面板功能可引用）/ `middleware` 可共享复用中间件 |
| `apps[].category` | 分类（面板按源聚合下发到分类筛选） |
| `apps[].logo` / `apps[].readme` | 仓库相对路径（同步时读入并入库） |
| `apps[].reverseProxy` | 一键反代端口 env key（如 `PANEL_APP_PORT`）；安装向导可填域名，安装后自动创建反代站点 |
| `apps[].website` / `apps[].sourceUrl` / `apps[].document` | 可选外链（官网/开源社区/文档），详情抽屉展示 |
| `apps[].versions[]` | 新版本放前面（第一条 = 最新，升级判定依据） |
| `versions[].package` | 仓库内包目录（git 源）或 tar.gz URL（远程源） |
| `versions[].env[]` | 参数定义 `{key,label,type(text/number/password/select),default,required,rule}` |
| `versions[].ports[]` | 端口定义 `{envKey,default}`（自动并入表单字段） |
| `versions[].middleware[]` | **M68 可复用中间件声明** `{type,prefix,required,label,minVersion}`——安装向导出现「中间件」下拉，只查找复用已有实例（不创建）：`type=s3/neo4j` 走数据库纳管实例（s3 自动建桶），其余类型走「容器 → 中间件」登记实例；选中后 `prefix` 前缀下的应用参数（`*_HOST/_PORT/_USER/_PASSWORD/_ENDPOINT` 等）自动接管注入。`minVersion` 低于基线的实例禁选 |
| `versions[].optionalServices[]` | **M68 可选伴生服务声明** `{id,label,compose,env}`——安装向导「可选组件」勾选区块：勾选后 `compose`（包内附加 compose 文件，网络占位同主文件）合并进主编排、`env`（如 `PLATFORM_X_ENABLED=true`）注入应用开关 |
| `versions[].pgExtensions[]` | 纳管 PG 自动创建的扩展（建库后 `CREATE EXTENSION IF NOT EXISTS`） |

## compose.yml 约定

- 变量渲染：`${VAR}`，来源 = 参数定义 default ∪ 用户输入；`CONTAINER_NAME` 自动注入（= `app-<应用名>`）
- 网络统一写 `1panel-network`（占位约定：面板安装时会整体替换为所选安装网络，默认 `ypanel_default`，与面板 nginx/站点互通，反代可用容器名直连）
- 版本包内文件统一纯文本（compose/配置模板），单文件 ≤2MB、总数 ≤200
- compose 文件名支持 `compose.yml` / `docker-compose.yml` 等，部署时统一落为 `docker-compose.yml`

## 图标版权

`apps/*/logo.*` 为各应用项目的品牌标识，版权归各自项目所有，仅用于应用商店中标识对应软件（参考 1Panel 等面板商店的惯例）。来源：优先取项目官方仓库/官网，部分取自 [dashboard-icons](https://github.com/homarr-labs/dashboard-icons) 与 iconify logos 集合。

## 维护（提交者）

本地仓库挂三个 remote（origin=GitHub / gitee / gitlab），每次更新同时推送三边，保持一致：

```bash
git push origin main && git push gitee main && git push gitlab main
```

## 本地联调

```bash
git clone https://gitee.com/mcyudream/YPanel-AppStore.git
# 面板源管理 → 编辑「YPanel 官方源」→ URL 填 file:///abs/path/YPanel-AppStore → 同步
```
