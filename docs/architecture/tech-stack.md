# 技术栈

本文档记录大云雀当前约定的技术栈。协作守则见 [CLAUDE.md](../../CLAUDE.md)，文档总索引见 [docs/README.md](../README.md)。

## 前端

- **框架**：Next.js 16 (App Router) + TypeScript
- **样式**：Tailwind CSS v4 + shadcn/ui
- **图表**：recharts
- **动画**：framer-motion
- **图标**：lucide-react

## 后端

- **框架**：FastAPI + Python
- **认证**：JWT
- **任务**：Redis 队列与轮询状态

## 数据导出

- **Excel**：exceljs
- **CSV**：原生 CSV

## 外部 API

- **多供应商 AI API**：通过 Provider 适配层统一调用。
- **供应商配置**：由管理员在后台维护 URL、Key、模型能力、成本、优先级与降级策略。

## 数据库

- **SQLite**：用户、配额、项目、模板、供应商、模型、任务等主数据。
- **Redis**：任务队列、任务状态、限流与缓存。
- **本地文件存储**：用户上传素材、生成结果与导出文件。

## 部署

- Docker Compose
- 服务端口：3300

## 版本控制

- Git
- GitHub
