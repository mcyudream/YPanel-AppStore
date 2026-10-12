# YuDream Admin

企业级管理平台（YuDream 自研）：后端 Java 21 / Spring Boot 3（DDD 分层），前端 Vue 3 + Arco Design，提供用户权限、内容管理、知识库、集成编排、可视化数据、AI Agent 等平台能力，插件运行时解耦业务。

安装向导支持：

- **MongoDB / Redis 纳管复用**：选择面板纳管实例自动建库建号并注入（Mongo 自动生成 `MONGO_URI`）
- **对象存储复用**：选择 RustFS/S3 纳管实例自动建桶并注入 `S3_*` 参数
- **可选组件**：消息渲染（render-server）、文件预览（kkFileView）、图数据库（Neo4j）按需勾选，自动并入编排并注入平台能力开关

安装后访问前端地址进入安装向导完成初始化（引导配置持久化在 `config/` 卷）。
