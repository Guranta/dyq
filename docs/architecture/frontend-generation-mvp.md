# 前端生成页面 MVP

本文档记录当前前端图片/视频生成页面 MVP。后端接口见 [后端 AI 调用接口 MVP](./backend-api-mvp.md)，实施计划见 [大云雀实施计划](../plans/2026-05-21-dayunque-plan.md)。

## 页面

- `/`：首页，展示创作入口和后端健康状态。
- `/create/image`：图片生成页面。
- `/create/video`：视频生成页面。

## 环境变量

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## 功能

- 调用 `POST /api/v1/generate/estimate` 展示预计消耗、供应商和模型。
- 调用 `POST /api/v1/generate/image` 创建图片生成任务。
- 调用 `POST /api/v1/generate/video` 创建视频生成任务。
- 使用 `GET /api/v1/tasks/{task_id}` 轮询任务状态。
- 展示图片结果或视频占位文件链接。

## 当前限制

- 尚未接入登录、用户配额和项目保存。
- 当前生成页面直接调用后端公开接口。
- 视频结果在 Mock Provider 下是文本占位文件，接真实视频供应商后会显示为视频预览。
