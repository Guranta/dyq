# 后端 AI 调用接口 MVP

本文档记录当前后端 AI 调用接口 MVP。相关计划见 [大云雀实施计划](../plans/2026-05-21-dayunque-plan.md)，技术栈见 [技术栈](./tech-stack.md)。

## 本地运行

```bash
cd server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 默认 Provider

默认使用 `mock` Provider，不需要真实 API Key，会生成本地占位图片 SVG 和视频占位文本文件，便于前后端先跑通接口。

如需接 OpenAI-compatible 中转供应商，可配置：

```bash
AI_PROVIDER=openai_compatible
AI_BASE_URL=https://example.com/v1
AI_API_KEY=your-api-key
AI_IMAGE_MODEL=image-model
AI_VIDEO_MODEL=video-model
AI_IMAGE_PATH=/images/generations
AI_VIDEO_PATH=/videos/generations
```

## 已实现接口

- `GET /api/v1/health`
- `GET /api/v1/providers`
- `POST /api/v1/generate/estimate`
- `POST /api/v1/generate/image`
- `POST /api/v1/generate/video`
- `GET /api/v1/tasks/{task_id}`

## 当前限制

- 当前任务状态存储为进程内内存，服务重启后任务记录会丢失。
- 当前默认生成结果由 Mock Provider 产生，用于跑通接口闭环。
- OpenAI-compatible Provider 只实现通用 URL 解析，具体供应商字段差异后续在供应商管理阶段细化。
- 当前尚未接入用户认证、配额扣减和数据库持久化。
