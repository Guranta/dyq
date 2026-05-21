# 大云雀

大云雀是一个用户友好型 AI 视频、图片与短剧创作平台。平台面向受邀用户开放创作能力，管理员负责创建用户、分配配额、配置模型供应商与监控任务。

## 项目文档

- [协作守则](./CLAUDE.md)
- [文档索引](./docs/README.md)

## 技术栈

- Next.js 16 (App Router) + TypeScript
- Tailwind CSS v4 + shadcn/ui
- recharts / framer-motion / lucide-react
- 多供应商 AI API 适配层
- FastAPI 后端服务
- SQLite + Redis + 本地文件存储
- Docker Compose 部署，端口 3300

详细技术栈见 [docs/architecture/tech-stack.md](./docs/architecture/tech-stack.md)。
