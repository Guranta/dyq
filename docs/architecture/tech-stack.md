# 技术栈

本文档记录 boltyapiEx 当前约定的技术栈。协作守则见 [CLAUDE.md](../../CLAUDE.md)，文档总索引见 [docs/README.md](../README.md)。

## 前端

- **框架**：Next.js 16 (App Router) + TypeScript
- **样式**：Tailwind CSS v4 + shadcn/ui
- **图表**：recharts
- **动画**：framer-motion
- **图标**：lucide-react

## 数据导出

- **Excel**：exceljs
- **CSV**：原生 CSV

## 外部 API

- **new-api 服务**：通过 Next.js API Route 代理调用。

## 数据库

- 当前为**无数据库纯代理模式**。
- `docker-compose.yml` 中预留 PostgreSQL，供未来扩展使用。

## 部署

- Docker Compose
- 服务端口：3300

## 版本控制

- Git
- GitHub
