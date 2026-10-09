# Adminer — 单文件数据库管理工具

PHP 应用类型（kind: php）的首个验收应用：一个 PHP 文件即完整功能，连接管理 MySQL/MariaDB/PostgreSQL/SQLite/ MongoDB 等数据库，轻量替代 phpMyAdmin。

## 使用

1. 安装后访问 `http://<站点地址>:<端口>/adminer.php`。
2. 服务器填数据库地址（同容器网络可用容器名，如 `app-mysql`；跨机填内网 IP）、用户名密码登录。
3. 登录页默认语言跟随浏览器，可在登录后切换。

## 说明

- 源码为官方 4.8.1 单文件（`source/adminer.php`），无需 composer/构建。
- 本应用只提供管理界面，不内置数据库；请配合商店 MySQL/PostgreSQL 应用或已有实例使用。
